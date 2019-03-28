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
import jinja2
import json_tricks


_HERE = os.path.dirname(__file__)

_html_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(_HERE, 'templates')))

_latex_env = jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string=r'}',
        variable_start_string=r'\VAR{',
        variable_end_string=r'}',
        comment_start_string=r'\#{',
        comment_end_string=r'}',
        line_statement_prefix=r'%%',
        line_comment_prefix=r'%#',
        trim_blocks=True,
        loader=jinja2.FileSystemLoader(os.path.join(_HERE, 'templates')))


class BaseElement(abc.ABC):
    # FIXME:
    # Alright, we want _html_template (_latex_template) to be required and act like:
    #    >>> self._html_template
    #    'template.html'
    # Which could be satisfied be a simple class attribute or a more complex property,
    # but NOT a method, which would have to be called like:
    #    >>> self._html_template()
    #    'template.html'
    # Unfortunately, the chained @property and @abc.abstractmethod doesn't enforce
    # an attribute/property like action and can be satisfied by defining a method,
    def __init__(self):
        if not isinstance(type(self)._html_template, property) and callable(self._html_template):
            raise TypeError('You must define an _html_template property or attribute for this class')
        if not isinstance(type(self)._latex_template, property) and callable(self._latex_template):
            raise TypeError('You must define an _latex_template property or attribute for this class')


    @property
    @abc.abstractmethod
    def _html_template(self):
        raise NotImplementedError


    @property
    @abc.abstractmethod
    def _latex_template(self):
        raise NotImplementedError


    def _repr_json(self):
        jsn = {type(self).__name__: self.__dict__}
        jsn[type(self).__name__].update({'__module__': type(self).__module__,
                                         '_html_template': self._html_template,
                                         '_latex_template': self._latex_template})
        return json_tricks.dumps(jsn, indent=4, primitives=True, allow_nan=True)


    def _repr_html(self):
        template = _html_env.get_template(self._html_template)
        return template.render(data=self.__dict__)


    def _repr_latex(self):
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


def gallery(title, image_elem_list):
    """
    Builds an image gallery out of a list of image elements. The
    gallery element is provided as a way of grouping images under
    a single heading and conserving space on the output page.

    Args:
        title: The title to display
        image_elem_list: The image elements to display.  If a single
            image element is given it will automatically be wrapped into
            a list.

    Returns:
        A dictionary with the metadata specifying that it is to be
        rendered as an image gallery
    """
    gal = {
        'Type': 'Gallery',
        'Title': title,
        'Data': image_elem_list,
    }
    return gal


class Image(BaseElement):
    _html_template = 'image.html'
    _latex_template = 'image.tex'

    def __init__(self, title, desc, image_file, group=None, height=None):
        super(Image, self).__init__()
        self.title = title
        self.desc = desc
        self.path, self.name = os.path.split(image_file)
        self.group = group
        self.height = height


def file_diff(title, diff_data):
    """
    Builds a file diff element.  This element can be used to check whether
    configuration files have changed or other similar checks.  Differences
    will be highlighted when rendered via Javascript.

    Args:
        title: The title to display
        diff_data: A dictionary of the form:
            { 'section_name' : { 'variable_name' : [diff, val_1, val_2] } }

    Returns:
        A dictionary with the metadata specifying that it is to be
        rendered as a file diff element
    """
    fd = {
        'Type': 'Diff',
        'Title': title,
        'Data': diff_data,
    }
    return fd


def error(title, error_msg):
    """
    Builds an error element.  Provides a way to show errors or other
    anomalous behavior in the web output.

    Args:
        title: The title to display
        error_msg: A description of the error or other helpful message

    Returns:
        A dictionary with the metadata specifying that it is to be
        rendered as an error element
    """
    err = {
        'Type': 'Error',
        'Title': title,
        'Message': error_msg,
    }
    return err


class RawHTML(BaseElement):
    _html_template = 'raw.html'
    _latex_template = 'raw.tex'

    def __init__(self, html):
        super(RawHTML, self).__init__()
        self.html = html
