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

import jinja2
import json_tricks

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
    """An abstract base LIVVkit Element

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
        jsn = {type(self).__name__: self.__dict__}
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


def book(title, description, page_dict=None):
    _book = {'Type': 'Book',
             'Title': title,
             'Description': description,
             }
    if page_dict is not None:
        _book['Data'] = page_dict

    return _book


def page(title, description, element_list=None, tab_list=None):
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
        tab_list: A list of tabs to display.

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
    if tab_list is not None:
        if isinstance(tab_list, list):
            _page['Data']['Tabs'] = tab_list
        else:
            _page['Data']['Tabs'] = [tab_list]
    return _page


def tab(tab_name, element_list=None, section_list=None):
    """
    Returns a dictionary representing a new tab to display elements.
    This can be thought of as a simple container for displaying multiple
    types of information.

    Args:
        tab_name: The title to display
        element_list: The list of elements to display. If a single element is
                      given it will be wrapped in a list.
        section_list: A list of sections to display.

    Returns:
        A dictionary with metadata specifying that it is to be rendered
        as a page containing multiple elements and/or tab.
    """
    _tab = {
        'Type': 'Tab',
        'Title': tab_name,
    }

    if element_list is not None:
        if isinstance(element_list, list):
            _tab['Elements'] = element_list
        else:
            _tab['Elements'] = [element_list]
    if section_list is not None:
        if isinstance(section_list, list):
            _tab['Sections'] = section_list
        else:
            if 'Elements' not in section_list:
                _tab['Elements'] = element_list
            else:
                _tab['Elements'].append(element_list)
    return _tab


def section(title, element_list):
    """
    Returns a dictionary representing a new section.  Sections
    contain a list of elements that are displayed separately from
    the global elements on the page.

    Args:
        title: The title of the section to be displayed
        element_list: The list of elements to display within the section

    Returns:
        A dictionary with metadata specifying that it is to be rendered as
        a section containing multiple elements
    """
    sect = {
        'Type': 'Section',
        'Title': title,
    }

    if isinstance(element_list, list):
        sect['Elements'] = element_list
    else:
        sect['Elements'] = [element_list]
    return sect


def table(title, headers, data_node):
    """
    Returns a dictionary representing a new table element.  Tables
    are specified with two main pieces of information, the headers
    and the data to put into the table.  Rendering of the table is
    the responsibility of the Javascript in the resources directory.
    When the data does not line up with the headers given this should
    be handled within the Javascript itself, not here.

    Args:
        title: The title to display
        headers: The columns to put into the table
        data_node: A dictionary with the form::
            {'case' : {'subcase' : { 'header' : data } } }

    Returns:
        A dictionary with the metadata specifying that it is to be
        rendered as a table.
    """
    tb = {
        'Type': 'Table',
        'Title': title,
        'Headers': headers,
        'Data': data_node,
    }
    return tb


def vtable(title, headers, data_node):
    """
    Returns a dictionary representing a new table element.  Tables
    are specified with two main pieces of information, the headers
    and the data to put into the table.  Rendering of the table is
    the responsibility of the Javascript in the resources directory.
    When the data does not line up with the headers given this should
    be handled within the Javascript itself, not here.

    Args:
        title: The title to display
        headers: The columns to put into the table
        data_node: A dictionary with the form::
            {'case' : {'subcase' : { 'header' : data } } }

    Returns:
        A dictionary with the metadata specifying that it is to be
        rendered as a table.
    """
    tb = {
        'Type': 'Vertical Table',
        'Title': title,
        'Headers': headers,
        'Data': data_node,
    }
    return tb


def bit_for_bit(title, headers, data_node):
    """
    Returns a dictionary representing a new bit for bit table element.
    Bit for bit elements can be thought of as tables, but require the
    special addition that a diff plot may need to be embedded within
    the table.

    Args:
        title: The title to display
        headers: Columns of the table
        data_node: A dictionary with the form:
            {'var_name' : {'header : { data } } }

    Returns:
        A dictionary with the metadata specifying that it is to be
        rendered as a bit for bit table
    """
    b4b = {
        'Type': 'Bit for Bit',
        'Title': title,
        'Headers': headers,
        'Data': data_node,
    }
    return b4b


class Gallery(BaseElement):
    _html_template = 'gallery.html'
    _latex_template = 'gallery.tex'

    def __init__(self, title, elements):
        super(Gallery, self).__init__()
        self.title = title
        self.elements = elements
        # FIXME: Remove once common.js is obsolete
        self.Type = 'Diff'
        self.Title = title
        self.Data = self._repr_html()

    def _repr_html(self):
        template = _html_env.get_template(self._html_template)
        elem_html = []
        for elem in self.elements:
            elem_html.append(elem._repr_html())

        return template.render(data=self.__dict__, elements=elem_html)

    def _repr_latex(self):
        template = _latex_env.get_template(self._latex_template)
        elem_tex = []
        for elem in self.elements:
            elem_tex.append(elem._repr_latex())

        return template.render(data=self.__dict__, elements=elem_tex)


class Image(BaseElement):
    _html_template = 'image.html'
    _latex_template = 'image.tex'

    def __init__(self, title, desc, image_file, group=None, height=None):
        super(Image, self).__init__()
        self.title = title
        self.desc = desc
        self.path, self.name = os.path.split(image_file)
        if not livvkit.index_dir:
            relative = os.getcwd()
            # TODO: Log a warning
        else:
            relative = os.path.dirname(livvkit.index_dir)
        self.path = os.path.sep + os.path.relpath(self.path, relative)
        self.group = group
        self.height = height

    def _repr_latex(self):
        template = _latex_env.get_template(self._latex_template)
        data = self.__dict__
        data['path'] = self.path.lstrip('/')
        return template.render(data=data)


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


class RawHTML(BaseElement):
    _html_template = 'raw.html'
    _latex_template = 'raw.tex'

    def __init__(self, html):
        super(RawHTML, self).__init__()
        self.html = html
        # FIXME: Remove once common.js is obsolete
        self.Type = 'HTML'
