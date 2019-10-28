# coding=utf-8
# Copyright (c) 2015-2018, UT-BATTELLE, LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Module to help building new display elements in the output
files easier and less error prone.

Implementing new elements is possible simply by adding new functions
They will be written out to the JSON files as sub-objects, which must
be interpreted by the Javascript found in the resources directory.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import abc
import difflib
import collections

import jinja2
import json_tricks
import pandas as pd

import livvkit

_HERE = os.path.dirname(__file__)

_html_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(_HERE, 'templates')))

_latex_env = jinja2.Environment(
        block_start_string=r'\BLOCK{',    # default: {%
        block_end_string=r'}',            # default: %}
        variable_start_string=r'\VAR{',   # default: {{
        variable_end_string=r'}',         # default: }}
        comment_start_string=r'\#{',      # default: {#
        comment_end_string=r'}',          # default: #}
        trim_blocks=True,
        loader=jinja2.FileSystemLoader(os.path.join(_HERE, 'templates')))


class BaseElement(abc.ABC):
    """An abstract base LIVVkit element

    An abstract base LIVVkit element providing the basic element interface
    expected by LIVVkit. All LIVVkit elements should either derive from this
    class or implement the same interface.
    """

    # FIXME: There's got to be a better way.
    #  We want _html_template (_latex_template) to be required and act like:
    #     >>> self._html_template
    #     'template.html'
    #  This could be satisfied be a simple class attribute or a more complex property,
    #  but NOT a method, which would have to be called like:
    #     >>> self._html_template()
    #     'template.html'
    #  Unfortunately, the chained @property and @abc.abstractmethod doesn't enforce
    #  an attribute/property like action and can be satisfied by defining a method,
    #  so we make sure that if it's not a property, it's also not callable (a method)
    def __init__(self):
        """Initialize a LIVVkit element
        """
        if not isinstance(type(self)._html_template, property) and callable(self._html_template):
            raise TypeError('You must define _html_template as a property or attribute for this class')
        if not isinstance(type(self)._latex_template, property) and callable(self._latex_template):
            raise TypeError('You must define _latex_template as a property or attribute for this class')

    @property
    @abc.abstractmethod
    def _html_template(self):
        """The jinja2 HTML template

        An attribute or property which holds the jinja2 template used to
        represent the element as HTML.

        Returns:
            str: The jinja2 HTML template
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _latex_template(self):
        """The jinja2 LaTeX template

        An attribute or property which holds the jinja2 template used to
        represent the element as LaTeX.

        Returns:
            str: The jinja2 LaTeX template
        """
        raise NotImplementedError

    def _repr_json(self):
        """Represent this element as JSON

        Using the internal dictionary representation of this element, return a
        JSON representation of this element

        Returns:
            str: The JSON representation of this element
        """
        jsn = {type(self).__name__: self.__dict__.copy()}
        jsn[type(self).__name__].update({'__module__': type(self).__module__,
                                         '_html_template': self._html_template,
                                         '_latex_template': self._latex_template})
        return json_tricks.dumps(jsn, indent=4, primitives=True, allow_nan=True)

    def _repr_html(self):
        """Represent this element as HTML

        Using the jinja2 template defined by ``self._html_template``, return an
        HTML representation of this element

        Returns:
            str: The HTML representation of this element
        """
        template = _html_env.get_template(self._html_template)
        return template.render(data=self.__dict__)

    def _repr_latex(self):
        """Represent this element as LaTeX

        Using the jinja2 template defined by ``self._latex_template``, return an
        LaTeX representation of this element

        Returns:
            str: The LaTeX representation of this element
        """
        template = _latex_env.get_template(self._latex_template)
        return template.render(data=self.__dict__)


class CompositeElement(BaseElement, abc.ABC):
    """An abstract base LIVVkit element that contains other elements

    An abstract base LIVVkit element that contains other elements in self.elements
    and provides the basic element interface expected by LIVVkit. All LIVVkit
    elements should either be derived from the LIVVkit BaseElement or implement
    the same interface.
    """
    def __init__(self, elements):
        """Initialize a composite LIVVkit element
        """
        super(CompositeElement, self).__init__()
        self.elements = elements

    def _repr_json(self):
        """Represent this element as JSON

        Using the internal dictionary representation of this element, return a
        JSON representation of this element

        Returns:
            str: The JSON representation of this element
        """
        jsn = {type(self).__name__: self.__dict__.copy()}
        jsn[type(self).__name__].update({'__module__': type(self).__module__,
                                         '_html_template': self._html_template,
                                         '_latex_template': self._latex_template})

        elem_repr = [elem._repr_json() for elem in self.elements]
        jsn[type(self).__name__]['elements'] = elem_repr

        return json_tricks.dumps(jsn, indent=4, primitives=True, allow_nan=True)

    def _repr_html(self):
        """Represent this element as HTML

        Using the jinja2 template defined by ``self._html_template``, return an
        HTML representation of this element

        Returns:
            str: The HTML representation of this element
        """
        elem_repr = [elem._repr_html() for elem in self.elements]
        template = _html_env.get_template(self._html_template)
        return template.render(data=self.__dict__, elements=elem_repr)

    def _repr_latex(self):
        """Represent this element as LaTeX

        Using the jinja2 template defined by ``self._latex_template``, return an
        LaTeX representation of this element

        Returns:
            str: The LaTeX representation of this element
        """
        template = _latex_env.get_template(self._latex_template)
        elem_repr = [elem._repr_latex() for elem in self.elements]
        return template.render(data=self.__dict__, elements=elem_repr)


class NamedCompositeElement(BaseElement, abc.ABC):
    """An abstract base LIVVkit element that contains multiple other composite elements

    An abstract base LIVVkit element that allows to logically group multiple
    other composite elements in self.element_dict and provides the basic element
    interface expected by LIVVkit. All LIVVkit elements should either be derived
    from the LIVVkit BaseElement or implement the same interface.
    """
    def __init__(self, elements_dict):
        """Initialize  a multi-composite LIVVkit element"""
        super(NamedCompositeElement, self).__init__()
        self.elements_dict = elements_dict

    def _repr_json(self):
        """Represent this element as JSON

        Using the internal dictionary representation of this element, return a
        JSON representation of this element

        Returns:
            str: The JSON representation of this element
        """
        jsn = {type(self).__name__: self.__dict__.copy()}
        jsn[type(self).__name__].update({'__module__': type(self).__module__,
                                         '_html_template': self._html_template,
                                         '_latex_template': self._latex_template})

        elem_repr = {}
        for title, elements in self.elements_dict.items():
            elem_repr[title] = [elem._repr_json() for elem in elements]

        jsn[type(self).__name__]['elements_dict'] = elem_repr

        return json_tricks.dumps(jsn, indent=4, primitives=True, allow_nan=True)

    def _repr_html(self):
        """Represent this element as HTML

        Using the jinja2 template defined by ``self._html_template``, return an
        HTML representation of this element

        Returns:
            str: The HTML representation of this element
        """
        elem_repr = {}
        for title, elements in self.elements_dict.items():
            elem_repr[title] = [elem._repr_html() for elem in elements]

        template = _html_env.get_template(self._html_template)
        return template.render(data=self.__dict__, elements_dict=elem_repr)

    def _repr_latex(self):
        """Represent this element as LaTeX

        Using the jinja2 template defined by ``self._latex_template``, return an
        LaTeX representation of this element

        Returns:
            str: The LaTeX representation of this element
        """
        elem_repr = {}
        for title, elements in self.elements_dict.items():
            elem_repr[title] = [elem._repr_latex() for elem in elements]

        template = _latex_env.get_template(self._latex_template)
        return template.render(data=self.__dict__, elements_dict=elem_repr)


def book(title, description, page_dict=None):
    _book = {'Type': 'Book',
             'Title': title,
             'Description': description,
             }
    if page_dict is not None:
        _book['Data'] = page_dict

    return _book


def page(title, description, element_list=None, tabs=None):
    """
    Returns a dictionary representing a new page to display elements.
    This can be thought of as a simple container for displaying multiple
    types of information. The ``section`` method can be used to create
    separate tabs.

    Args:
        title: The title to display
        description: A description of the section
        element_list: The list of elements to display. If a single element is
                      given it will be wrapped in a list.
        tabs: A LIVVkit Tabs element containing the tabs to display on the page

    Returns:
        A dictionary with metadata specifying that it is to be rendered
        as a page containing multiple elements and/or tabs.
    """
    _page = {
        'Type': 'Page',
        'Title': title,
        'Description': description,
        'Data': {},
    }

    if element_list is not None:
        if isinstance(element_list, list):
            _page['Data']['Elements'] = element_list
        else:
            _page['Data']['Elements'] = [element_list]
    if tabs is not None:
        _page['Data']['Tabs'] = tabs.__dict__

    return _page


# FIXME: Docstring --> pass in a dictionary like {tab_title: [tab_elements]}
class Tabs(NamedCompositeElement):
    _html_template = 'tabs.html'
    _latex_template = 'tabs.tex'

    def __init__(self, tabs):
        super(Tabs, self).__init__(tabs)
        # FIXME: Remove once common.js is obsolete
        self.Data = self._repr_html()


class Section(CompositeElement):
    _html_template = 'section.html'
    _latex_template = 'section.tex'

    def __init__(self, title, elements):
        super(Section, self).__init__(elements)
        self.title = title
        # FIXME: Remove once common.js is obsolete
        self.Type = 'Gallery'
        self.Title = title
        self.Data = self._repr_html()


class Table(BaseElement):
    _html_template = 'table.html'
    _latex_template = 'table.tex'

    # FIXME: Typehinting and docstring for data, which should look like
    #        {header1:[val1, val2...],... }
    #
    #        Index = True --> use pandas index or simply number the rows
    #        Index = False --> No index
    #        Index = iterable (list) --> override index with iterable
    #
    #        Transpose = False --> do nothing
    #        Transpose = True  --> flip table so header is a column and index is a row
    def __init__(self, title, data, index=False, transpose=False):
        super(Table, self).__init__()
        self.title = title

        if isinstance(data, pd.DataFrame):
            self.data = data.to_dict(orient='list')
            self.index = data.index.to_list()
        else:
            self.data = data
            self.index = None

        self.rows = len(next(iter(self.data.values())))

        if index is True and self.index is None:
            self.index = range(self.rows)
        elif isinstance(index, collections.abc.Collection):
            if len(index) != self.rows:
                raise IndexError('Table index must be the same length as the table. '
                                 'Table rows: {}, index length: {}.'.format(self.rows, len(index)))
            self.index = index

        if transpose:
            self._html_template = 'table_transposed.html'
            self._latex_template = 'table_transposed.tex'

        # FIXME: Remove once common.js is obsolete
        self.Type = 'Table'
        self.Title = self.title
        self.Headers = list(self.data.keys())
        self.Data = self._repr_html()

    def _repr_html(self):
        """Represent this element as HTML

        Using the jinja2 template defined by ``self._html_template``, return an
        HTML representation of this element

        Returns:
            str: The HTML representation of this element
        """
        template = _html_env.get_template(self._html_template)
        return template.render(data=self.__dict__, rows=self.rows, index=self.index)

    def _repr_latex(self):
        """Represent this element as LaTeX

        Using the jinja2 template defined by ``self._latex_template``, return an
        LaTeX representation of this element

        Returns:
            str: The LaTeX representation of this element
        """
        template = _latex_env.get_template(self._latex_template)
        return template.render(data=self.__dict__, rows=self.rows, index=self.index)


class BitForBit(CompositeElement):
    _html_template = 'bit4bit.html'
    _latex_template = 'bit4bit.tex'

    def __init__(self, title, data, imgs):
        super(BitForBit, self).__init__(imgs)
        self.title = title

        if isinstance(data, pd.DataFrame):
            self.data = data.to_dict(orient='list')
        else:
            self.data = data

        self.rows = len(next(iter(self.data.values())))
        if len(imgs) != self.rows:
            raise IndexError('Imgs must be the same length as the table. '
                             'Table rows: {}, imgs length: {}.'.format(self.rows, len(imgs)))

        # FIXME: Remove once common.js is obsolete
        self.Type = "Bit for Bit"
        self.Title = title
        self.Data = self._repr_html()

    def _repr_html(self):
        """Represent this element as HTML

        Using the jinja2 template defined by ``self._html_template``, return an
        HTML representation of this element

        Returns:
            str: The HTML representation of this element
        """
        imgs_repr = [img._repr_html() for img in self.elements]
        template = _html_env.get_template(self._html_template)
        return template.render(data=self.__dict__, rows=self.rows, b4b_imgs=imgs_repr)

    def _repr_latex(self):
        """Represent this element as LaTeX

        Using the jinja2 template defined by ``self._latex_template``, return an
        LaTeX representation of this element

        Returns:
            str: The LaTeX representation of this element
        """
        imgs_repr = [img._repr_latex() for img in self.elements]
        template = _latex_env.get_template(self._latex_template)
        return template.render(data=self.__dict__, rows=self.rows, b4b_imgs=imgs_repr)


class Gallery(CompositeElement):
    _html_template = 'gallery.html'
    _latex_template = 'gallery.tex'

    def __init__(self, title, elements):
        super(Gallery, self).__init__(elements)
        self.title = title
        # FIXME: Remove once common.js is obsolete
        self.Type = 'Gallery'
        self.Title = title
        self.Data = self._repr_html()


class Image(BaseElement):
    _html_template = 'image.html'
    _latex_template = 'image.tex'

    def __init__(self, title, desc, image_file, group=None, height=None, relative_to=None):
        super(Image, self).__init__()
        self.title = title
        self.desc = desc
        self.path, self.name = os.path.split(image_file)
        # FIXME: This assumes that images are images are always located in a
        #        subdirectory of the current page if a relative path start
        #        location isn't specified
        if relative_to is None:
            relative_to = os.path.dirname(self.path)
        self.path = os.path.relpath(self.path, relative_to)
        self.group = group
        self.height = height

    def _repr_latex(self):
        template = _latex_env.get_template(self._latex_template)
        data = self.__dict__
        data['path'] = self.path.lstrip('/')
        return template.render(data=data)


class B4BImage(Image):
    def __init__(self, title, description, page_path):
        image_file = os.path.join(livvkit.output_dir, 'imgs', 'b4b.png')

        super(B4BImage, self).__init__(title, description,
                                       image_file=image_file,
                                       relative_to=page_path,
                                       height=50, group='b4b')


class NAImage(Image):
    def __init__(self, title, description, page_path):
        image_file = os.path.join(livvkit.output_dir, 'imgs', 'na.png')

        super(NAImage, self).__init__(title, description,
                                      image_file=image_file,
                                      relative_to=page_path,
                                      height=50, group='na')


class FileDiff(BaseElement):
    _html_template = 'diff.html'
    _latex_template = 'diff.tex'

    def __init__(self, title, from_file, to_file, context=3):
        super(FileDiff, self).__init__()
        self.title = title
        self.from_file = from_file
        self.to_file = to_file
        self.diff, self.diff_status = self.diff_files(context=context)
        # FIXME: Remove once common.js is obsolete
        self.Type = 'Diff'
        self.Title = title
        self.Data = self._repr_html()

    def diff_files(self, context=3):
        with open(self.from_file) as from_, open(self.to_file) as to_:
            fromlines = from_.read().splitlines()
            tolines = to_.read().splitlines()

            if context is None:
                context = max(len(fromlines), len(tolines))

            diff = list(difflib.unified_diff(fromlines, tolines,
                                             n=context,  lineterm=''))
            diff_status = True
            if not diff:
                diff_status = False
                diff = fromlines
            return diff, diff_status


class Error(BaseElement):
    _html_template = 'err.html'
    _latex_template = 'err.tex'

    def __init__(self, title, message):
        super(Error, self).__init__()
        self.title = title
        self.message = message
        # FIXME: Remove once common.js is obsolete
        self.Type = 'Error'
        self.Data = self._repr_html()


class RawHTML(BaseElement):
    _html_template = 'raw.html'
    _latex_template = 'raw.tex'

    def __init__(self, html):
        super(RawHTML, self).__init__()
        self.html = html
        # FIXME: Remove once common.js is obsolete
        self.Type = 'HTML'
