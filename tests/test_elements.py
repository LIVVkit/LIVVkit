# coding=utf-8

"""Test the LIVVkit elements"""

import json
from contextlib import ContextDecorator

import pytest

import livvkit
from livvkit import elements


class LIVVkitOutput(ContextDecorator):
    """Decorator to set the required livvkit variable `livvkit.output_dir`"""
    def __enter__(self):
        livvkit.output_dir = 'vv_test'

    def __exit__(self, exc_type, exc_val, exc_tb):
        livvkit.output_dir = None


def test_el_base_templates_as_property():
    truth = 'template_string'

    class Property(elements.BaseElement):
        """Class to test property definition of _*_template"""
        @property
        def _html_template(self):
            return truth

        @property
        def _latex_template(self):
            return truth

    p = Property()

    errors = []
    if p._html_template != truth:
        errors.append("Error:_html_template doesn't act like a property")
    if p._latex_template != truth:
        errors.append("Error:_latex_template doesn't act like a property")

    assert not errors, 'These errors occurred:\n    {}'.format(
            '\n    '.join(errors))


def test_el_base_templates_as_class_attribute():
    errors = []
    truth = 'template_string'

    class ClassAttribute(elements.BaseElement):
        """Class to test attribute definition of _*_template"""
        _html_template = truth
        _latex_template = truth

    ca = ClassAttribute()

    if ca._html_template != truth:
        errors.append("Error:_html_template doesn't act like a class attribute")
    if ca._latex_template != truth:
        errors.append("Error:_latex_template doesn't act like a class attribute")

    assert not errors, 'These errors occurred:\n    {}'.format(
            '\n    '.join(errors))


def test_el_base_templates_as_instance_attribute():
    truth = 'template_string'

    class HTMLInstanceAttribute(elements.BaseElement):
        """Class to test instance attribute definition of _*_template"""
        def __init__(self, html):
            self._html_template = html
            super(HTMLInstanceAttribute, self).__init__()

        @property
        def _latex_template(self):
            return truth

    class LatexInstanceAttribute(elements.BaseElement):
        def __init__(self, latex):
            self._latex_template = latex
            super(LatexInstanceAttribute, self).__init__()

        @property
        def _html_template(self):
            return truth

    with pytest.raises(TypeError):
        _ = HTMLInstanceAttribute(truth)

    with pytest.raises(TypeError):
        _ = LatexInstanceAttribute(truth)


def test_el_base_templates_as_method():
    truth = 'template_string'

    class HTMLMethod(elements.BaseElement):
        """Class to test method definition of _*_template"""
        def _html_template(self):
            return truth

        @property
        def _latex_template(self):
            return truth

    class LatexMethod(elements.BaseElement):
        """Class to test method definition of _*_template"""
        @property
        def _html_template(self):
            return truth

        def _latex_template(self):
            return truth

    with pytest.raises(TypeError):
        _ = HTMLMethod()

    with pytest.raises(TypeError):
        _ = LatexMethod()


def test_el_page_json():
    truth = '{\n' \
            '    "Page": {\n' \
            '        "elements": [\n' \
            '            {\n' \
            '                "Section": {\n' \
            '                    "elements": [\n' \
            '                        {\n' \
            '                            "Table": {\n' \
            '                                "title": "title",\n' \
            '                                "data": {\n' \
            '                                    "h1": [\n' \
            '                                        "v1",\n' \
            '                                        "v2"\n' \
            '                                    ],\n' \
            '                                    "h2": [\n' \
            '                                        "v3",\n' \
            '                                        "v4"\n' \
            '                                    ]\n' \
            '                                },\n' \
            '                                "index": null,\n' \
            '                                "rows": 2,\n' \
            '                                "__module__": "livvkit.elements.elements",\n' \
            '                                "_html_template": "table.html",\n' \
            '                                "_latex_template": "table.tex"\n' \
            '                            }\n' \
            '                        }\n' \
            '                    ],\n' \
            '                    "title": "A cool table",\n' \
            '                    "__module__": "livvkit.elements.elements",\n' \
            '                    "_html_template": "section.html",\n' \
            '                    "_latex_template": "section.tex"\n' \
            '                }\n' \
            '            }\n' \
            '        ],\n' \
            '        "title": "A Page",\n' \
            '        "description": "A good description",\n' \
            '        "_ref_list": null,\n' \
            '        "Data": "<div id=\\"A Page\\">\\n    <h2>A Page</h2>\\n    <p>A good description</p>\\n    <div class=\\"section\\">\\n    <h2>A cool table</h2>\\n    <div class=\\"table\\">\\n    <h3>title</h3>\\n    <table>\\n        <tr>\\n            <th>h1</th>\\n            <th>h2</th>\\n        </tr>\\n        <tr>\\n            <td>v1</td>\\n            <td>v3</td>\\n        </tr>\\n        <tr>\\n            <td>v2</td>\\n            <td>v4</td>\\n        </tr>\\n    </table>\\n</div>\\n</div>\\n</div>",\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "page.html",\n' \
            '        "_latex_template": "page.tex"\n' \
            '    }\n' \
            '}'

    page = elements.Page(
        'A Page', 'A good description',
        [elements.Section('A cool table', [elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})])],
        references=None,
    )

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(page._repr_json())

    assert page._repr_json() == truth


def test_el_page_html():
    truth = '<div id="A Page">\n' \
            '    <h2>A Page</h2>\n' \
            '    <p>A good description</p>\n' \
            '    <div class="section">\n' \
            '    <h2>A cool table</h2>\n' \
            '    <div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>h1</th>\n' \
            '            <th>h2</th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>v1</td>\n' \
            '            <td>v3</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>v2</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>\n' \
            '</div>\n' \
            '</div><div class="bibliography"><h2>References</h2><p>LIVVkit is an open source project licensed under a BSD 3-clause License. We ask that you please acknowledge LIVVkit in any work it is used or supports. In any corresponding published work, please cite: </p><dl><dt>1</dt> <dd>K.&nbsp;J. Evans, J.&nbsp;H. Kennedy, D.&nbsp;Lu, M.&nbsp;M. Forrester, S.&nbsp;Price, J.&nbsp;Fyke, A.&nbsp;R. Bennett, M.&nbsp;J. Hoffman, I.&nbsp;Tezaur, C.&nbsp;S. Zender, and M.&nbsp;Vizca\\\'<span class="bibtex-protected">ı</span>no. Livvkit 2.1: automated and extensible ice sheet model validation. <em>Geoscientific Model Development</em>, 12(3):1067–1086, 2019. URL: <a href="https://www.geosci-model-dev.net/12/1067/2019/">https://www.geosci-model-dev.net/12/1067/2019/</a>, <a href="https://doi.org/10.5194/gmd-12-1067-2019">doi:10.5194/gmd-12-1067-2019</a>.</dd> <dt>2</dt> <dd>Joseph&nbsp;H. Kennedy, Andrew&nbsp;R. Bennett, Katherine&nbsp;J. Evans, Stephen Price, Matthew Hoffman, William&nbsp;H. Lipscomb, Jeremy Fyke, Lauren Vargo, Adrianna Boghozian, Matthew Norman, and Patrick&nbsp;H. Worley. Livvkit: an extensible, python-based, land ice verification and validation toolkit for ice sheet models. <em>Journal of Advances in Modeling Earth Systems</em>, 9(2):854–869, 2017. <a href="https://doi.org/10.1002/2017MS000916">doi:10.1002/2017MS000916</a>.</dd> </dl></div>'


    page = elements.Page(
        'A Page', 'A good description',
        [elements.Section('A cool table', [elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})])]
    )

    assert page._repr_html() == truth


def test_el_page_latex():
    truth = "\\levelstay{A Page}\n" \
            "A good description\n" \
            "    \\levelstay{A cool table}\n" \
            "    \\begin{table}[h!]\n" \
            "    \\centering\n" \
            "    \\begin{tabular}{cc}\n" \
            "        h1 & h2 \\\\\n" \
            "        \\hline\n" \
            "        v1 & v3  \\\\\n" \
            "        v2 & v4  \\\\\n" \
            "        \\end{tabular}\n" \
            "\\end{table}\n" \
            "\n" \
            "\\begin{thebibliography}{1}\n" \
            "\n" \
            "\\bibitem[1]{gmd-12-1067-2019}\n" \
            "K.~J. Evans, J.~H. Kennedy, D.~Lu, M.~M. Forrester, S.~Price, J.~Fyke, A.~R. Bennett, M.~J. Hoffman, I.~Tezaur, C.~S. Zender, and M.~Vizca\\'{ı}no.\n" \
            "\\newblock Livvkit 2.1: automated and extensible ice sheet model validation.\n" \
            "\\newblock \\emph{Geoscientific Model Development}, 12(3):1067–1086, 2019.\n" \
            "\\newblock URL: \\url{https://www.geosci-model-dev.net/12/1067/2019/}, \\href{https://doi.org/10.5194/gmd-12-1067-2019}{doi:10.5194/gmd-12-1067-2019}.\n" \
            "\n" \
            "\\bibitem[2]{Kennedy2017}\n" \
            "Joseph~H. Kennedy, Andrew~R. Bennett, Katherine~J. Evans, Stephen Price, Matthew Hoffman, William~H. Lipscomb, Jeremy Fyke, Lauren Vargo, Adrianna Boghozian, Matthew Norman, and Patrick~H. Worley.\n" \
            "\\newblock Livvkit: an extensible, python-based, land ice verification and validation toolkit for ice sheet models.\n" \
            "\\newblock \\emph{Journal of Advances in Modeling Earth Systems}, 9(2):854–869, 2017.\n" \
            "\\newblock \\href{https://doi.org/10.1002/2017MS000916}{doi:10.1002/2017MS000916}.\n" \
            "\n" \
            "\\end{thebibliography}\n"

    page = elements.Page(
        'A Page', 'A good description',
        [elements.Section('A cool table', [elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})])]
    )

    assert page._repr_latex() == truth


def test_el_tabs_json():
    truth = '{\n' \
            '    "Tabs": {\n' \
            '        "elements_dict": {\n' \
            '            "a": [\n' \
            '                {\n' \
            '                    "Error": {\n' \
            '                        "title": "AError",\n' \
            '                        "message": "woops",\n' \
            '                        "__module__": "livvkit.elements.elements",\n' \
            '                        "_html_template": "err.html",\n' \
            '                        "_latex_template": "err.tex"\n' \
            '                    }\n' \
            '                }\n' \
            '            ],\n' \
            '            "b": [\n' \
            '                {\n' \
            '                    "Error": {\n' \
            '                        "title": "BError",\n' \
            '                        "message": "boogers",\n' \
            '                        "__module__": "livvkit.elements.elements",\n' \
            '                        "_html_template": "err.html",\n' \
            '                        "_latex_template": "err.tex"\n' \
            '                    }\n' \
            '                }\n' \
            '            ]\n' \
            '        },\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "tabs.html",\n' \
            '        "_latex_template": "tabs.tex"\n' \
            '    }\n' \
            '}'

    tabs = elements.Tabs(
        {'a': [elements.Error('AError', 'woops')], 'b': [elements.Error('BError', 'boogers')]}
    )

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(tabs._repr_json())

    assert tabs._repr_json() == truth


def test_el_tabs_html():
    truth = '<div id="tabs">\n' \
            '    <ul>\n' \
            '        <li><a href="#a">a</a></li>\n' \
            '        <li><a href="#b">b</a></li>\n' \
            '    </ul>\n' \
            '    <div id="a">\n' \
            '        <div class="error">\n' \
            '    <h3>AError</h3>\n' \
            '    <p>woops</p>\n' \
            '</div>\n' \
            '    </div>\n' \
            '    <div id="b">\n' \
            '        <div class="error">\n' \
            '    <h3>BError</h3>\n' \
            '    <p>boogers</p>\n' \
            '</div>\n' \
            '    </div>\n' \
            '</div>'

    tabs = elements.Tabs({'a': [elements.Error('AError', 'woops')], 'b': [elements.Error('BError', 'boogers')]})

    assert tabs._repr_html() == truth


def test_el_tabs_latex():
    truth = '\\levelstay{a}\n' \
            '    \\colorbox{red}{\\parbox{\\textwidth}{\n' \
            '    \\textbf{AError}: woops\n' \
            '}}\\levelstay{b}\n' \
            '    \\colorbox{red}{\\parbox{\\textwidth}{\n' \
            '    \\textbf{BError}: boogers\n' \
            '}}'

    tabs = elements.Tabs({'a': [elements.Error('AError', 'woops')], 'b': [elements.Error('BError', 'boogers')]})

    assert tabs._repr_latex() == truth


def test_el_section_json():
    truth = '{\n' \
            '    "Section": {\n' \
            '        "elements": [\n' \
            '            {\n' \
            '                "Table": {\n' \
            '                    "title": "title",\n' \
            '                    "data": {\n' \
            '                        "h1": [\n' \
            '                            "v1",\n' \
            '                            "v2"\n' \
            '                        ],\n' \
            '                        "h2": [\n' \
            '                            "v3",\n' \
            '                            "v4"\n' \
            '                        ]\n' \
            '                    },\n' \
            '                    "index": null,\n' \
            '                    "rows": 2,\n' \
            '                    "__module__": "livvkit.elements.elements",\n' \
            '                    "_html_template": "table.html",\n' \
            '                    "_latex_template": "table.tex"\n' \
            '                }\n' \
            '            }\n' \
            '        ],\n' \
            '        "title": "A cool table",\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "section.html",\n' \
            '        "_latex_template": "section.tex"\n' \
            '    }\n' \
            '}'

    section = elements.Section('A cool table', [elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})])

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(section._repr_json())

    assert section._repr_json() == truth


def test_el_section_html():
    truth = '<div class="section">\n' \
            '    <h2>A cool table</h2>\n' \
            '    <div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>h1</th>\n' \
            '            <th>h2</th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>v1</td>\n' \
            '            <td>v3</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>v2</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>\n' \
            '</div>'

    section = elements.Section('A cool table', [elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})])

    assert section._repr_html() == truth


def test_el_section_latex():
    truth = '\\levelstay{A cool table}\n' \
            '    \\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{cc}\n' \
            '        h1 & h2 \\\\\n' \
            '        \\hline\n' \
            '        v1 & v3  \\\\\n' \
            '        v2 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}\n'

    section = elements.Section('A cool table', [elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})])

    assert section._repr_latex() == truth


def test_el_table_json():
    truth = '{\n' \
            '    "Table": {\n' \
            '        "title": "title",\n' \
            '        "data": {\n' \
            '            "h1": [\n' \
            '                "v1",\n' \
            '                "v2"\n' \
            '            ],\n' \
            '            "h2": [\n' \
            '                "v3",\n' \
            '                "v4"\n' \
            '            ]\n' \
            '        },\n' \
            '        "index": null,\n' \
            '        "rows": 2,\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "table.html",\n' \
            '        "_latex_template": "table.tex"\n' \
            '    }\n' \
            '}'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(table._repr_json())

    assert table._repr_json() == truth


def test_el_table_html():
    truth = '<div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>h1</th>\n' \
            '            <th>h2</th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>v1</td>\n' \
            '            <td>v3</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>v2</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})

    assert table._repr_html() == truth


def test_el_table_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{cc}\n' \
            '        h1 & h2 \\\\\n' \
            '        \\hline\n' \
            '        v1 & v3  \\\\\n' \
            '        v2 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})

    assert table._repr_latex() == truth


def test_el_table_w_index_html():
    truth = '<div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>&nbsp;</th>\n' \
            '            <th>h1</th>\n' \
            '            <th>h2</th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>0</th>\n' \
            '            <td>v1</td>\n' \
            '            <td>v3</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>1</th>\n' \
            '            <td>v2</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=True)

    assert table._repr_html() == truth


def test_el_table_w_index_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{ r | cc}\n' \
            '         & h1 & h2 \\\\\n' \
            '        \\hline\n' \
            '        0 & v1 & v3  \\\\\n' \
            '        1 & v2 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=True)

    assert table._repr_latex() == truth


def test_el_table_w_custom_index_html():
    truth = '<div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>&nbsp;</th>\n' \
            '            <th>h1</th>\n' \
            '            <th>h2</th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>i0</th>\n' \
            '            <td>v1</td>\n' \
            '            <td>v3</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>i1</th>\n' \
            '            <td>v2</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=['i0', 'i1'])

    assert table._repr_html() == truth


def test_el_table_w_custom_index_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{ r | cc}\n' \
            '         & h1 & h2 \\\\\n' \
            '        \\hline\n' \
            '        i0 & v1 & v3  \\\\\n' \
            '        i1 & v2 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=['i0', 'i1'])

    assert table._repr_latex() == truth


def test_el_table_transposed_html():
    truth = '<div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>h1</th>\n' \
            '            <td>v1</td>\n' \
            '            <td>v2</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>h2</th>\n' \
            '            <td>v3</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, transpose=True)

    assert table._repr_html() == truth


def test_el_table_transposed_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{r|cc}\n' \
            '        h1 & v1 & v2  \\\\\n' \
            '        h2 & v3 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, transpose=True)

    assert table._repr_latex() == truth


def test_el_table_w_index_transposed_html():
    truth = '<div class="table">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>&nbsp;</th>\n' \
            '            <th>0</th>\n' \
            '            <th>1</th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>h1</th>\n' \
            '            <td>v1</td>\n' \
            '            <td>v2</td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <th>h2</th>\n' \
            '            <td>v3</td>\n' \
            '            <td>v4</td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']},
                           index=True, transpose=True)

    assert table._repr_html() == truth


def test_el_table_w_index_transposed_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{r|cc}\n' \
            '         & 0 & 1\\\\\n' \
            '        \\hline\n' \
            '        h1 & v1 & v2  \\\\\n' \
            '        h2 & v3 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    table = elements.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']},
                           index=True, transpose=True)

    assert table._repr_latex() == truth


@LIVVkitOutput()
def test_el_b4b_json():
    truth = '{\n' \
            '    "BitForBit": {\n' \
            '        "elements": [\n' \
            '            {\n' \
            '                "B4BImage": {\n' \
            '                    "title": "",\n' \
            '                    "desc": "desc.",\n' \
            '                    "path": "../imgs",\n' \
            '                    "name": "b4b.png",\n' \
            '                    "group": "b4b",\n' \
            '                    "height": 50,\n' \
            '                    "__module__": "livvkit.elements.elements",\n' \
            '                    "_html_template": "image.html",\n' \
            '                    "_latex_template": "image.tex"\n' \
            '                }\n' \
            '            },\n' \
            '            {\n' \
            '                "B4BImage": {\n' \
            '                    "title": "",\n' \
            '                    "desc": "desc.",\n' \
            '                    "path": "../imgs",\n' \
            '                    "name": "b4b.png",\n' \
            '                    "group": "b4b",\n' \
            '                    "height": 50,\n' \
            '                    "__module__": "livvkit.elements.elements",\n' \
            '                    "_html_template": "image.html",\n' \
            '                    "_latex_template": "image.tex"\n' \
            '                }\n' \
            '            }\n' \
            '        ],\n' \
            '        "title": "title",\n' \
            '        "data": {\n' \
            '            "Variable": [\n' \
            '                "velnorm",\n' \
            '                "thk"\n' \
            '            ],\n' \
            '            "Max Error": [\n' \
            '                5.0707,\n' \
            '                0.376806\n' \
            '            ],\n' \
            '            "Index of Max Error": [\n' \
            '                [\n' \
            '                    2,\n' \
            '                    1,\n' \
            '                    24,\n' \
            '                    19\n' \
            '                ],\n' \
            '                [\n' \
            '                    3,\n' \
            '                    23,\n' \
            '                    23\n' \
            '                ]\n' \
            '            ],\n' \
            '            "RMS Error": [\n' \
            '                0.260977,\n' \
            '                0.0354492\n' \
            '            ]\n' \
            '        },\n' \
            '        "rows": 2,\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "bit4bit.html",\n' \
            '        "_latex_template": "bit4bit.tex"\n' \
            '    }\n' \
            '}'

    b4b = elements.BitForBit(
        'title', {'Variable': ['velnorm', 'thk'],
                  'Max Error': [5.07070, 0.376806],
                  'Index of Max Error': [(2, 1, 24, 19), (3, 23, 23)],
                  'RMS Error': [.260977, .0354492],
                  },
        imgs=[elements.B4BImage('', 'desc.', page_path='vv_test/verification'),
              elements.B4BImage('', 'desc.', page_path='vv_test/verification'),
              ]
    )

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(b4b._repr_json())

    assert b4b._repr_json() == truth


@LIVVkitOutput()
def test_el_b4b_html():
    truth = '<div class="bitForBit">\n' \
            '    <h3>title</h3>\n' \
            '    <table>\n' \
            '        <tr>\n' \
            '            <th>Variable</th>\n' \
            '            <th>Max Error</th>\n' \
            '            <th>Index of Max Error</th>\n' \
            '            <th>RMS Error</th>\n' \
            '            <th> Plot </th>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>velnorm</td>\n' \
            '            <td>5.07070e+00</td>\n' \
            '            <td>(2, 1, 24, 19)</td>\n' \
            '            <td>2.60977e-01</td>\n' \
            '            <td>\n' \
            '                <div>\n' \
            '    <a href="../imgs/b4b.png"\n' \
            '       data-lightbox="b4b"\n' \
            '       data-title="desc."\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption=""\n' \
            '             alt=""\n' \
            '             src="../imgs/b4b.png"\n' \
            '             style="height: 50px; overflow: hidden; position: relative;"\n' \
            '        >\n' \
            '    </a>\n' \
            '</div>\n' \
            '            </td>\n' \
            '        </tr>\n' \
            '        <tr>\n' \
            '            <td>thk</td>\n' \
            '            <td>3.76806e-01</td>\n' \
            '            <td>(3, 23, 23)</td>\n' \
            '            <td>3.54492e-02</td>\n' \
            '            <td>\n' \
            '                <div>\n' \
            '    <a href="../imgs/b4b.png"\n' \
            '       data-lightbox="b4b"\n' \
            '       data-title="desc."\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption=""\n' \
            '             alt=""\n' \
            '             src="../imgs/b4b.png"\n' \
            '             style="height: 50px; overflow: hidden; position: relative;"\n' \
            '        >\n' \
            '    </a>\n' \
            '</div>\n' \
            '            </td>\n' \
            '        </tr>\n' \
            '    </table>\n' \
            '</div>'

    b4b = elements.BitForBit(
        'title', {'Variable': ['velnorm', 'thk'],
                  'Max Error': [5.07070, 0.376806],
                  'Index of Max Error': [(2, 1, 24, 19), (3, 23, 23)],
                  'RMS Error': [.260977, .0354492],
                  },
        imgs=[elements.B4BImage('', 'desc.', page_path='vv_test/verification'),
              elements.B4BImage('', 'desc.', page_path='vv_test/verification'),
              ]
    )

    assert b4b._repr_html() == truth


@LIVVkitOutput()
def test_el_b4b_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{ c  c  c  c  c }\n' \
            '        Variable & Max Error & Index of Max Error & RMS Error & Plots \\\\\n' \
            '        \\hline\n' \
            '        velnorm & 5.07070e+00 & (2, 1, 24, 19) & 2.60977e-01 & \\begin{minipage}{0.3\\textwidth}\\begin{figure}[h]\n' \
            '    \\centering\n' \
            '    \\includegraphics[height=50px]{../imgs/b4b.png}\n' \
            '    \\caption[]{desc.}\n' \
            '\\end{figure}\\end{minipage} \\\\\n' \
            '        thk & 3.76806e-01 & (3, 23, 23) & 3.54492e-02 & \\begin{minipage}{0.3\\textwidth}\\begin{figure}[h]\n' \
            '    \\centering\n' \
            '    \\includegraphics[height=50px]{../imgs/b4b.png}\n' \
            '    \\caption[]{desc.}\n' \
            '\\end{figure}\\end{minipage} \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    b4b = elements.BitForBit(
        'title', {'Variable': ['velnorm', 'thk'],
                  'Max Error': [5.07070, 0.376806],
                  'Index of Max Error': [(2, 1, 24, 19), (3, 23, 23)],
                  'RMS Error': [.260977, .0354492],
                  },
        imgs=[elements.B4BImage('', 'desc.', page_path='vv_test/verification'),
              elements.B4BImage('', 'desc.', page_path='vv_test/verification'),
              ]
    )

    assert b4b._repr_latex() == truth

    livvkit.output_dir = None


def test_el_gallery_json():
    truth = '{\n' \
            '    "Gallery": {\n' \
            '        "elements": [\n' \
            '            {\n' \
            '                "Image": {\n' \
            '                    "title": "The Image",\n' \
            '                    "desc": "A very nice image.",\n' \
            '                    "path": "imgs",\n' \
            '                    "name": "image.png",\n' \
            '                    "group": null,\n' \
            '                    "height": null,\n' \
            '                    "__module__": "livvkit.elements.elements",\n' \
            '                    "_html_template": "image.html",\n' \
            '                    "_latex_template": "image.tex"\n' \
            '                }\n' \
            '            }\n' \
            '        ],\n' \
            '        "title": "The Gallery",\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "gallery.html",\n' \
            '        "_latex_template": "gallery.tex"\n' \
            '    }\n' \
            '}'

    image = elements.Image('The Image', 'A very nice image.', 'imgs/image.png')
    gallery = elements.Gallery('The Gallery', [image])

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(gallery._repr_json())

    assert gallery._repr_json() == truth


def test_el_gallery_html():
    truth = '<div class="gallery">\n' \
            '    <h3>The Gallery</h3>\n' \
            '    <div>\n' \
            '    <a href="imgs/image.png"\n' \
            '       data-lightbox="The Image"\n' \
            '       data-title="A very nice image."\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption="The Image"\n' \
            '             alt="The Image"\n' \
            '             src="imgs/image.png"\n' \
            '             style="height: 200px; overflow: hidden; position: relative;"\n' \
            '        >\n' \
            '    </a>\n' \
            '</div>\n' \
            '    \n' \
            '</div>\n' \
            '<div style="clear:both"></div>'

    image = elements.Image('The Image', 'A very nice image.', 'imgs/image.png')
    gallery = elements.Gallery('The Gallery', [image])

    assert gallery._repr_html() == truth


def test_el_gallery_latex():
    truth = '\\levelstay{The Gallery}\n' \
            '    \\begin{figure}[h]\n' \
            '    \\centering\n' \
            '    \\includegraphics[height=200px]{imgs/image.png}\n' \
            '    \\caption[The Image]{A very nice image.}\n' \
            '\\end{figure}\n'

    image = elements.Image('The Image', 'A very nice image.', 'imgs/image.png')
    gallery = elements.Gallery('The Gallery', [image])

    assert gallery._repr_latex() == truth


def test_el_image_json():
    truth = '{\n' \
            '    "Image": {\n' \
            '        "title": "title",\n' \
            '        "desc": "description",\n' \
            '        "path": "imgs",\n' \
            '        "name": "name.png",\n' \
            '        "group": "group",\n        "height": 300,\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "image.html",\n' \
            '        "_latex_template": "image.tex"\n' \
            '    }\n' \
            '}'

    image = elements.Image('title', 'description', 'imgs/name.png', group='group', height=300)

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(image._repr_json())

    assert image._repr_json() == truth


def test_el_image_html():
    truth = '<div>\n' \
            '    <a href="imgs/name.png"\n' \
            '       data-lightbox="group"\n' \
            '       data-title="description"\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption="title"\n' \
            '             alt="title"\n' \
            '             src="imgs/name.png"\n' \
            '             style="height: 300px; overflow: hidden; position: relative;"\n' \
            '        >\n' \
            '    </a>\n' \
            '</div>'

    image = elements.Image('title', 'description', 'imgs/name.png', group='group', height=300)

    assert image._repr_html() == truth


def test_el_image_latex():
    truth = "\\begin{figure}[h]\n" \
            "    \\centering\n" \
            "    \\includegraphics[height=300px]{imgs/name.png}\n" \
            "    \\caption[title]{description}\n" \
            "\\end{figure}"

    image = elements.Image('title', 'description', 'imgs/name.png', group='group', height=300)

    assert image._repr_latex() == truth


def test_el_file_diff_json(diff_data):
    from_file, to_file = diff_data

    with open(from_file) as from_:
        fromlines = from_.read().splitlines()

    diff_diff = elements.FileDiff('Test JSON', from_file=from_file, to_file=to_file)
    diff_same = elements.FileDiff('Test JSON', from_file=from_file, to_file=from_file)
    errors = []

    if diff_diff.diff_status is not True or diff_diff.diff == fromlines:
        errors.append('Error: there was no difference between the files.')
    if diff_same.diff_status is True or diff_same.diff != fromlines:
        errors.append('Error: Self difference showed a difference.')

    try:
        _ = json.loads(diff_diff._repr_json())
    except json.JSONDecodeError:
        errors.append('Diff_diff element did not produce valid JSON.')

    try:
        _ = json.loads(diff_same._repr_json())
    except json.JSONDecodeError:
        errors.append('Diff_same element did not produce valid JSON.')

    assert not errors, 'Errors occurred:\n{}'.format('\n'.join(errors))


def test_el_file_diff_html(diff_data):
    truth = '<h3>Test HTML</h3>\n' \
            '<div class="diff">\n' \
            '    <p class="old">--- </p>\n' \
            '    <p class="new">+++ </p>\n' \
            '    <p class="range">@@ -4,7 +4,7 @@</p>\n' \
            '    <p> upn = 10</p>\n' \
            '    <p> ewn = 31</p>\n' \
            '    <p> nsn = 31</p>\n' \
            '    <p class="old">-dew = 2000.0</p>\n' \
            '    <p class="new">+dew = 200.0</p>\n' \
            '    <p> dns = 2000.0</p>\n' \
            '    <p> </p>\n' \
            '    <p> [time]</p>\n' \
            '</div>'

    from_file, to_file = diff_data

    diff = elements.FileDiff('Test HTML', from_file=from_file, to_file=to_file)

    assert diff._repr_html() == truth


def test_el_file_diff_latex(diff_data):
    truth = '\\begin{minted}{diff}\n' \
            '--- \n' \
            '+++ \n' \
            '@@ -4,7 +4,7 @@\n' \
            ' upn = 10\n' \
            ' ewn = 31\n' \
            ' nsn = 31\n' \
            '-dew = 2000.0\n' \
            '+dew = 200.0\n' \
            ' dns = 2000.0\n' \
            ' \n' \
            ' [time]\n' \
            '\\end{minted}'

    from_file, to_file = diff_data

    diff = elements.FileDiff('Test HTML', from_file=from_file, to_file=to_file)

    assert diff._repr_latex() == truth


def test_el_error_json():
    truth = '{\n' \
            '    "Error": {\n' \
            '        "title": "WOOPS",\n' \
            '        "message": "Mistakes were made.",\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "err.html",\n' \
            '        "_latex_template": "err.tex"\n' \
            '    }\n' \
            '}'

    err = elements.Error('WOOPS', 'Mistakes were made.')

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(err._repr_json())

    assert err._repr_json() == truth


def test_el_error_html():
    truth = '<div class="error">\n' \
            '    <h3>WOOPS</h3>\n' \
            '    <p>Mistakes were made.</p>\n' \
            '</div>'

    err = elements.Error('WOOPS', 'Mistakes were made.')

    assert err._repr_html() == truth


def test_el_error_latex():
    truth = '\\colorbox{red}{\\parbox{\\textwidth}{\n' \
            '    \\textbf{WOOPS}: Mistakes were made.\n' \
            '}}'
    err = elements.Error('WOOPS', 'Mistakes were made.')

    assert err._repr_latex() == truth


def test_el_raw_html_json():
    truth = '{\n' \
            '    "RawHTML": {\n' \
            '        "html": "<div>Hi</div>",\n' \
            '        "__module__": "livvkit.elements.elements",\n' \
            '        "_html_template": "raw.html",\n' \
            '        "_latex_template": "raw.tex"\n' \
            '    }\n' \
            '}'

    html = elements.RawHTML('<div>Hi</div>')

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(html._repr_json())

    assert html._repr_json() == truth


def test_el_raw_html_html():
    truth = '<div>\n    <div>Hi</div>\n</div>'

    html = elements.RawHTML('<div>Hi</div>')

    assert html._repr_html() == truth


def test_el_raw_html_latex():
    truth = '\\begin{minted}{html}\n    <div>Hi</div>\n\\end{minted}'

    html = elements.RawHTML('<div>Hi</div>')

    assert html._repr_latex() == truth
