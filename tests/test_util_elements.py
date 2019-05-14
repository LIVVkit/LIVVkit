# coding=utf-8

"""Test the LIVVkit elements"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from livvkit.util import elements as el


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
    assert False


def test_el_table_html():
    assert False


def test_el_vtable_json():
    assert False


def test_el_vtable_html():
    assert False


def test_el_vhtable_json():
    assert False


def test_el_vhtable_html():
    assert False


def test_el_b4b_json():
    assert False


def test_el_b4b_html():
    assert False


def test_el_gallery_json():
    assert False


def test_el_gallery_html():
    assert False


def test_el_image_json():
    truth = '{\n' \
            '    "Image": {\n' \
            '        "title": "title",\n' \
            '        "desc": "description",\n' \
            '        "path": "path",\n' \
            '        "name": "name.png",\n' \
            '        "group": "group",\n        "height": 300,\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "image.html",\n' \
            '        "_latex_template": "image.tex"\n' \
            '    }\n' \
            '}'

    image = el.Image('title', 'description', 'path/name.png', group='group', height=300)

    assert truth == image._repr_json()


def test_el_image_html():
    truth = '<div>\n' \
            '    <a href="path/name.png"\n' \
            '       data-lightbox="group"\n' \
            '       data-title="description"\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption="title"\n' \
            '             alt="title"\n' \
            '             src="path/name.png"\n' \
            '             style="height: 300px; overflow: hidden; position: relative;"\n' \
            '        >\n' \
            '    </a>\n' \
            '</div>'

    image = el.Image('title', 'description', 'path/name.png', group='group', height=300)

    assert truth == image._repr_html()


def test_el_image_latex():
    truth = "\\begin{figure}[h]\n" \
            "    \\centering\n" \
            "    \\includegraphics[height=300px]{path/name.png}\n" \
            "    \\caption[title]{description}\n" \
            "\\end{figure}"

    image = el.Image('title', 'description', 'path/name.png', group='group', height=300)

    assert truth == image._repr_latex()


def test_el_file_diff_json():
    assert False


def test_el_file_diff_html():
    assert False


def test_el_error_json():
    truth = '{\n' \
            '    "Error": {\n' \
            '        "Type": "Error",\n' \
            '        "title": "WOOPS",\n' \
            '        "message": "Mistakes were made.",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "err.html",\n' \
            '        "_latex_template": "err.tex"\n' \
            '    }\n' \
            '}'

    err = el.Error('WOOPS', 'Mistakes were made.')

    assert truth == err._repr_json()


def test_el_error_html():
    truth = '<div class="error">\n' \
            '    <h3>WOOPS</h3>\n' \
            '    <p>Mistakes were made.</p>\n' \
            '</div>'

    err = el.Error('WOOPS', 'Mistakes were made.')

    assert truth == err._repr_html()


def test_el_error_latex():
    truth = '\\colorbox{red}{\\parbox{\\textwidth}{\n' \
            '    \\textbf{WOOPS}: Mistakes were made.\n' \
            '}}'
    err = el.Error('WOOPS', 'Mistakes were made.')

    assert truth == err._repr_latex()


def test_el_raw_html_json():
    truth = '{\n' \
            '    "RawHTML": {\n' \
            '        "Type": "HTML",\n' \
            '        "html": "<div>Hi</div>",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "raw.html",\n' \
            '        "_latex_template": "raw.tex"\n' \
            '    }\n' \
            '}'

    html = el.RawHTML('<div>Hi</div>')

    assert truth == html._repr_json()


def test_el_raw_html_html():
    truth = '<div>\n    <div>Hi</div>\n</div>'

    html = el.RawHTML('<div>Hi</div>')

    assert truth == html._repr_html()


def test_el_raw_html_latex():
    truth = '\\begin{minted}{html}\n    <div>Hi</div>\n\\end{minted}'

    html = el.RawHTML('<div>Hi</div>')

    assert truth == html._repr_latex()
