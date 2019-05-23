# coding=utf-8

"""Test the LIVVkit elements"""

from __future__ import absolute_import, print_function, unicode_literals

import json

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
    errors = []
    elements = []
    for ii in range(3):
        elements.append(el.Image('Image {}'.format(ii),
                                 'The {}-th image.'.format(ii),
                                 'imgs/image{}.png'.format(ii)))

    gallery = el.Gallery('An image gallery', elements=elements)

    try:
        _ = json.loads(gallery._repr_json())
    except json.JSONDecodeError:
        errors.append('Error: Gallery element did not produce valid JSON.')

    truth = '{\n' \
            '    "Gallery": {\n' \
            '        "title": "Empty",\n' \
            '        "elements": [],\n' \
            '        "Type": "Diff",\n' \
            '        "Title": "Empty",\n' \
            '        "Data": "<div class=\\"gallery\\">\\n    <h3>Empty</h3>\\n    \\n</div>\\n<div style=\\"clear:both\\"></div>",\n' \
            '        "__module__": "livvkit.util.elements.elements",\n' \
            '        "_html_template": "gallery.html",\n' \
            '        "_latex_template": "gallery.tex"\n' \
            '    }\n' \
            '}'

    empty_gallery = el.Gallery('Empty', [])

    if empty_gallery._repr_json() != truth:
        errors.append('Error: JSON representation of Gallery element has changed.')

    assert not errors, 'Errors occurred:\n{}'.format('\n'.join(errors))


def test_el_gallery_html():
    truth = '<div class="gallery">\n' \
            '    <h3>The Gallery</h3>\n' \
            '    <div>\n' \
            '    <a href="/imgs/image.png"\n' \
            '       data-lightbox="The Image"\n' \
            '       data-title="A very nice image."\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption="The Image"\n' \
            '             alt="The Image"\n' \
            '             src="/imgs/image.png"\n' \
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
            '        "path": "/path",\n' \
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
            '    <a href="/path/name.png"\n' \
            '       data-lightbox="group"\n' \
            '       data-title="description"\n' \
            '    >\n' \
            '        <img class="thumbnail caption"\n' \
            '             data-caption="title"\n' \
            '             alt="title"\n' \
            '             src="/path/name.png"\n' \
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
            '        "html": "<div>Hi</div>",\n' \
            '        "Type": "HTML",\n' \
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
