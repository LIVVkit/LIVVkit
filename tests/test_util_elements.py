# coding=utf-8

"""Test the LIVVkit elements"""

from __future__ import absolute_import, print_function, unicode_literals

import json
from contextlib import ContextDecorator

import pytest

import livvkit
from livvkit.util import elements as el


class LIVVkitOutput(ContextDecorator):
    def __enter__(self):
        livvkit.output_dir = 'vv_test'

    def __exit__(self, exc_type, exc_val, exc_tb):
        livvkit.output_dir = None


def test_el_base_templates_as_property():
    truth = 'template_string'

    # noinspection PyMissingOrEmptyDocstring
    class Property(el.BaseElement):
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

    # noinspection PyMissingOrEmptyDocstring
    class ClassAttribute(el.BaseElement):
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

    # noinspection PyMissingOrEmptyDocstring,PyAbstractClass
    class HTMLInstanceAttribute(el.BaseElement):
        def __init__(self, html):
            # noinspection PyPropertyAccess
            self._html_template = html
            super(HTMLInstanceAttribute, self).__init__()

        @property
        def _latex_template(self):
            return truth

    # noinspection PyMissingOrEmptyDocstring,PyAbstractClass
    class LatexInstanceAttribute(el.BaseElement):
        def __init__(self, latex):
            # noinspection PyPropertyAccess
            self._latex_template = latex
            super(LatexInstanceAttribute, self).__init__()

        @property
        def _html_template(self):
            return truth

    with pytest.raises(TypeError):
        # noinspection PyUnusedLocal
        hia = HTMLInstanceAttribute(truth)

    with pytest.raises(TypeError):
        # noinspection PyUnusedLocal
        lia = LatexInstanceAttribute(truth)


def test_el_base_templates_as_method():
    truth = 'template_string'

    # noinspection PyMissingOrEmptyDocstring
    class HTMLMethod(el.BaseElement):
        def _html_template(self):
            return truth

        @property
        def _latex_template(self):
            return truth

    # noinspection PyMissingOrEmptyDocstring
    class LatexMethod(el.BaseElement):
        @property
        def _html_template(self):
            return truth

        def _latex_template(self):
            return truth

    with pytest.raises(TypeError):
        # noinspection PyUnusedLocal
        hm = HTMLMethod()

    with pytest.raises(TypeError):
        # noinspection PyUnusedLocal
        lm = LatexMethod()


def test_el_book_json():
    assert False


def test_el_book_html():
    assert False


def test_el_page_json():
    assert False


def test_el_page_html():
    assert False


def test_el_tab_json():
    assert False


def test_el_tab_html():
    assert False


def test_el_section_json():
    assert False


def test_el_section_html():
    assert False


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
            '        "Type": "Table",\n' \
            '        "Title": "title",\n' \
            '        "Headers": [\n' \
            '            "h1",\n' \
            '            "h2"\n' \
            '        ],\n' \
            '        "Data": "<div class=\\"table\\">\\n    <h3>title</h3>\\n    <table>\\n        <tr>\\n            <th>h1</th>\\n            <th>h2</th>\\n        </tr>\\n        <tr>\\n            <td>v1</td>\\n            <td>v3</td>\\n        </tr>\\n        <tr>\\n            <td>v2</td>\\n            <td>v4</td>\\n        </tr>\\n    </table>\\n</div>",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "table.html",\n' \
            '        "_latex_template": "table.tex"\n' \
            '    }\n' \
            '}'


    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']})

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=True)

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=True)

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=['i0', 'i1'])

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, index=['i0', 'i1'])

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, transpose=True)

    assert table._repr_html() == truth


def test_el_table_transposed_latex():
    truth = '\\begin{table}[h!]\n' \
            '    \\centering\n' \
            '    \\begin{tabular}{r|cc}\n' \
            '        h1 & v1 & v2  \\\\\n' \
            '        h2 & v3 & v4  \\\\\n' \
            '        \\end{tabular}\n' \
            '\\end{table}'

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, transpose=True)

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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']},
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

    table = el.Table('title', {'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']},
                     index=True, transpose=True)

    assert table._repr_latex() == truth


@LIVVkitOutput()
def test_el_b4b_json():
    truth = '{\n' \
            '    "BitForBit": {\n' \
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
            '        "b4b_imgs": [\n' \
            '            "{\\n    \\"B4BImage\\": {\\n        \\"title\\": \\"\\",\\n        \\"desc\\": \\"desc.\\",\\n        \\"path\\": \\"../imgs\\",\\n        \\"name\\": \\"b4b.png\\",\\n        \\"group\\": null,\\n        \\"height\\": 50,\\n        \\"__module__\\": \\"livvkit.util.elements.elements\\",\\n        \\"_html_template\\": \\"image.html\\",\\n        \\"_latex_template\\": \\"image.tex\\"\\n    }\\n}",\n' \
            '            "{\\n    \\"B4BImage\\": {\\n        \\"title\\": \\"\\",\\n        \\"desc\\": \\"desc.\\",\\n        \\"path\\": \\"../imgs\\",\\n        \\"name\\": \\"b4b.png\\",\\n        \\"group\\": null,\\n        \\"height\\": 50,\\n        \\"__module__\\": \\"livvkit.util.elements.elements\\",\\n        \\"_html_template\\": \\"image.html\\",\\n        \\"_latex_template\\": \\"image.tex\\"\\n    }\\n}"\n' \
            '        ],\n' \
            '        "Type": "Bit for Bit",\n' \
            '        "Title": "title",\n' \
            '        "Data": "<div class=\\"bitForBit\\">\\n    <h3>title</h3>\\n    <table>\\n        <tr>\\n            <th>Variable</th>\\n            <th>Max Error</th>\\n            <th>Index of Max Error</th>\\n            <th>RMS Error</th>\\n            <th> Plot </th>\\n        </tr>\\n        <tr>\\n            <td>velnorm</td>\\n            <td>5.07070e+00</td>\\n            <td>(2, 1, 24, 19)</td>\\n            <td>2.60977e-01</td>\\n            <td>\\n                <div>\\n    <a href=\\"../imgs/b4b.png\\"\\n       data-lightbox=\\"\\"\\n       data-title=\\"desc.\\"\\n    >\\n        <img class=\\"thumbnail caption\\"\\n             data-caption=\\"\\"\\n             alt=\\"\\"\\n             src=\\"../imgs/b4b.png\\"\\n             style=\\"height: 50px; overflow: hidden; position: relative;\\"\\n        >\\n    </a>\\n</div>\\n            </td>\\n        </tr>\\n        <tr>\\n            <td>thk</td>\\n            <td>3.76806e-01</td>\\n            <td>(3, 23, 23)</td>\\n            <td>3.54492e-02</td>\\n            <td>\\n                <div>\\n    <a href=\\"../imgs/b4b.png\\"\\n       data-lightbox=\\"\\"\\n       data-title=\\"desc.\\"\\n    >\\n        <img class=\\"thumbnail caption\\"\\n             data-caption=\\"\\"\\n             alt=\\"\\"\\n             src=\\"../imgs/b4b.png\\"\\n             style=\\"height: 50px; overflow: hidden; position: relative;\\"\\n        >\\n    </a>\\n</div>\\n            </td>\\n        </tr>\\n    </table>\\n</div>",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "bit4bit.html",\n' \
            '        "_latex_template": "bit4bit.tex"\n' \
            '    }\n' \
            '}'


    b4b = el.BitForBit('title', {'Variable': ['velnorm', 'thk'],
                                 'Max Error': [5.07070, 0.376806],
                                 'Index of Max Error': [(2, 1, 24, 19), (3, 23, 23)],
                                 'RMS Error': [.260977, .0354492]},
                       imgs=[el.B4BImage('', 'desc.', page_path='vv_test/verification'),
                             el.B4BImage('', 'desc.', page_path='vv_test/verification')])

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
            '       data-lightbox=""\n' \
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
            '       data-lightbox=""\n' \
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

    b4b = el.BitForBit('title', {'Variable': ['velnorm', 'thk'],
                                 'Max Error': [5.07070, 0.376806],
                                 'Index of Max Error': [(2, 1, 24, 19), (3, 23, 23)],
                                 'RMS Error': [.260977, .0354492]},
                       imgs=[el.B4BImage('', 'desc.', page_path='vv_test/verification'),
                             el.B4BImage('', 'desc.', page_path='vv_test/verification')])

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

    b4b = el.BitForBit('title', {'Variable': ['velnorm', 'thk'],
                                 'Max Error': [5.07070, 0.376806],
                                 'Index of Max Error': [(2, 1, 24, 19), (3, 23, 23)],
                                 'RMS Error': [.260977, .0354492]},
                       imgs=[el.B4BImage('', 'desc.', page_path='vv_test/verification'),
                             el.B4BImage('', 'desc.', page_path='vv_test/verification')])

    assert b4b._repr_latex() == truth

    livvkit.output_dir = None


def test_el_gallery_json():
    truth = '{\n' \
            '    "Gallery": {\n' \
            '        "title": "The Gallery",\n' \
            '        "elements": [\n' \
            '            "{\\n    \\"Image\\": {\\n        \\"title\\": \\"The Image\\",\\n        \\"desc\\": \\"A very nice image.\\",\\n        \\"path\\": \\"imgs\\",\\n        \\"name\\": \\"image.png\\",\\n        \\"group\\": null,\\n        \\"height\\": null,\\n        \\"__module__\\": \\"livvkit.util.elements.elements\\",\\n        \\"_html_template\\": \\"image.html\\",\\n        \\"_latex_template\\": \\"image.tex\\"\\n    }\\n}"\n' \
            '        ],\n' \
            '        "Type": "Gallery",\n' \
            '        "Title": "The Gallery",\n' \
            '        "Data": "<div class=\\"gallery\\">\\n    <h3>The Gallery</h3>\\n    <div>\\n    <a href=\\"imgs/image.png\\"\\n       data-lightbox=\\"The Image\\"\\n       data-title=\\"A very nice image.\\"\\n    >\\n        <img class=\\"thumbnail caption\\"\\n             data-caption=\\"The Image\\"\\n             alt=\\"The Image\\"\\n             src=\\"imgs/image.png\\"\\n             style=\\"height: 200px; overflow: hidden; position: relative;\\"\\n        >\\n    </a>\\n</div>\\n    \\n</div>\\n<div style=\\"clear:both\\"></div>",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "gallery.html",\n' \
            '        "_latex_template": "gallery.tex"\n' \
            '    }\n' \
            '}'

    image = el.Image('The Image', 'A very nice image.', 'imgs/image.png')
    gallery = el.Gallery('The Gallery', [image])

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

    image = el.Image('The Image', 'A very nice image.', 'imgs/image.png')
    gallery = el.Gallery('The Gallery', [image])

    assert gallery._repr_html() == truth


def test_el_gallery_latex():
    truth = '\\levelstay{The Gallery}\n' \
            '    \\begin{figure}[h]\n' \
            '    \\centering\n' \
            '    \\includegraphics[height=200px]{imgs/image.png}\n' \
            '    \\caption[The Image]{A very nice image.}\n' \
            '\\end{figure}\n'

    image = el.Image('The Image', 'A very nice image.', 'imgs/image.png')
    gallery = el.Gallery('The Gallery', [image])

    assert gallery._repr_latex() == truth


def test_el_image_json():
    truth = '{\n' \
            '    "Image": {\n' \
            '        "title": "title",\n' \
            '        "desc": "description",\n' \
            '        "path": "imgs",\n' \
            '        "name": "name.png",\n' \
            '        "group": "group",\n        "height": 300,\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "image.html",\n' \
            '        "_latex_template": "image.tex"\n' \
            '    }\n' \
            '}'

    image = el.Image('title', 'description', 'imgs/name.png', group='group', height=300)

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

    image = el.Image('title', 'description', 'imgs/name.png', group='group', height=300)

    assert image._repr_html() == truth


def test_el_image_latex():
    truth = "\\begin{figure}[h]\n" \
            "    \\centering\n" \
            "    \\includegraphics[height=300px]{imgs/name.png}\n" \
            "    \\caption[title]{description}\n" \
            "\\end{figure}"

    image = el.Image('title', 'description', 'imgs/name.png', group='group', height=300)

    assert image._repr_latex() == truth


def test_el_file_diff_json(diff_data):
    from_file, to_file = diff_data

    with open(from_file) as from_:
        fromlines = from_.read().splitlines()

    diff_diff = el.FileDiff('Test JSON', from_file=from_file, to_file=to_file)
    diff_same = el.FileDiff('Test JSON', from_file=from_file, to_file=from_file)
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

    diff = el.FileDiff('Test HTML', from_file=from_file, to_file=to_file)

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

    diff = el.FileDiff('Test HTML', from_file=from_file, to_file=to_file)

    assert diff._repr_latex() == truth


def test_el_error_json():
    truth = '{\n' \
            '    "Error": {\n' \
            '        "title": "WOOPS",\n' \
            '        "message": "Mistakes were made.",\n' \
            '        "Type": "Error",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "err.html",\n' \
            '        "_latex_template": "err.tex"\n' \
            '    }\n' \
            '}'

    err = el.Error('WOOPS', 'Mistakes were made.')

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(err._repr_json())

    assert err._repr_json() == truth


def test_el_error_html():
    truth = '<div class="error">\n' \
            '    <h3>WOOPS</h3>\n' \
            '    <p>Mistakes were made.</p>\n' \
            '</div>'

    err = el.Error('WOOPS', 'Mistakes were made.')

    assert err._repr_html() == truth


def test_el_error_latex():
    truth = '\\colorbox{red}{\\parbox{\\textwidth}{\n' \
            '    \\textbf{WOOPS}: Mistakes were made.\n' \
            '}}'
    err = el.Error('WOOPS', 'Mistakes were made.')

    assert err._repr_latex() == truth


def test_el_raw_html_json():
    truth = '{\n' \
            '    "RawHTML": {\n' \
            '        "html": "<div>Hi</div>",\n' \
            '        "Type": "HTML",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "raw.html",\n' \
            '        "_latex_template": "raw.tex"\n' \
            '    }\n' \
            '}'

    html = el.RawHTML('<div>Hi</div>')

    # Will raise a JSONDecodeError if not valid JSON
    _ = json.loads(html._repr_json())

    assert html._repr_json() == truth


def test_el_raw_html_html():
    truth = '<div>\n    <div>Hi</div>\n</div>'

    html = el.RawHTML('<div>Hi</div>')

    assert html._repr_html() == truth


def test_el_raw_html_latex():
    truth = '\\begin{minted}{html}\n    <div>Hi</div>\n\\end{minted}'

    html = el.RawHTML('<div>Hi</div>')

    assert html._repr_latex() == truth
