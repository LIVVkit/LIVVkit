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

# FIXME: This docstring
"""Module containing report generation and display elements

The elements in this module are used by LIVVkit to generate analyses reports.
Reports by default will be a portable HTML website, but each of these elements
provide some experimental (and therefore undocumented) report formats: JSON-Only
and LaTeX.

New elements should derive from, or implement the same interface as, the
BaseElement abstract class.
"""

import os
import abc
import glob
import difflib
import collections

from pathlib import Path

import jinja2
import json_tricks
import pandas as pd

import livvkit
import livvkit.data
from livvkit.util import bib

_HERE = os.path.dirname(__file__)

# skipcq: BAN-B701
_html_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(_HERE, 'templates')))

# skipcq: BAN-B701
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

        Args:
            elements: A list of LIVVkit elements
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

        elem_repr = [json_tricks.loads(elem._repr_json()) for elem in self.elements]
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
        """Initialize  a multi-composite LIVVkit element

        Args:
            elements_dict: A dictionary where the (key, value) item represents a
             collection of LIVVkit elements. The key should be a name for the
             collection and the value should be a list of elements.
        """
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
            elem_repr[title] = [json_tricks.loads(elem._repr_json()) for elem in elements]

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


class Page(CompositeElement):
    """A LIVVkit Page element

    The Page element contains the description of an analysis, the elements
    that should be displayed for this analysis on the report, as well as any
    references that should be included in the report. In general usage, this
    will be used to create an HTML page inside LIVVkit output website. It also
    will allow for the generation of other (experimental!) Report types
    (e.g., LaTeX), where the "page" meaning might be better interpreted as
    a "section".

    For LIVVkit Extensions (LEX), an instance of this class should be returned
    from the extensions `run()` function.
    """
    _html_template = 'page.html'
    _latex_template = 'page.tex'

    def __init__(self, title, description, elements, references=''):
        """Initialize a Page elements

        Args:
            title: the title to display on the analysis
            description: A long (paragraph or more) description of the analysis
                being performed. Typically, it's best to write this description
                as the LEX extension's docstring and pass this class `__doc__`
            elements: A list of LIVVkit elements to include in the report
            references: The references to include as part of this analysis. This
                can be a path to a bibtex file containing the references, or a
                list/set/tuple of bibtex files containing the references (Note:
                ALL references inside the bibtex file(s) will be included!). Default
                value is `references=''` which will cause only the default LIVVkit
                references to be displayed. References can be entirely removed by
                setting `references=None`, however, this is *not* recommended.
        """
        super(Page, self).__init__(elements)
        self.title = title
        self.description = description
        self._ref_list = None
        if references is not None:
            self.add_references(references)
        # FIXME: remove once common.js is obsolete
        self.Data = self._repr_html()

    def add_references(self, references):
        """Add a reference to the internal reference list

        Args:
            references: The references to add to this page's internal reference
                list. This can be a path to a bibtex file containing the
                references, or a list/set/tuple of bibtex files containing the
                references (Note: This will include the default LIVVkit
                references and ALL references inside the bibtex file(s)!).
        """
        if self._ref_list is None:
            self._ref_list = glob.glob(
                os.path.join(os.path.dirname(livvkit.data.__file__), '*.bib')
            )

        if references:
            if isinstance(references, (str, Path)):
                self._ref_list.append(references)
            elif isinstance(references, (list, set, tuple)):
                self._ref_list += list(references)
            else:
                raise NotImplementedError(
                    'Cannot add {} type to the reference list. References must be either a (str or '
                    'Path) path to a bibtex file, or a list/set/tuple of bibtex files.'.format(type(references))
                )

    def _repr_html(self):
        """Represent this element as HTML

        Using the jinja2 template defined by ``self._html_template``, return an
        HTML representation of this element

        Returns:
            str: The HTML representation of this element
        """
        template = _html_env.get_template(self._html_template)
        elem_repr = [elem._repr_html() for elem in self.elements]
        rendered_html = template.render(data=self.__dict__, elements=elem_repr)
        if self._ref_list is not None:
            rendered_html += bib.bib2html(self._ref_list)

        return rendered_html

    def _repr_latex(self):
        """Represent this element as LaTeX

        Using the jinja2 template defined by ``self._latex_template``, return an
        LaTeX representation of this element

        Returns:
            str: The LaTeX representation of this element
        """
        template = _latex_env.get_template(self._latex_template)
        elem_repr = [elem._repr_latex() for elem in self.elements]
        rendered_tex = template.render(data=self.__dict__, elements=elem_repr)

        # FIXME: This is hacky! We're cheating the livvkit.util.bib.bib2html
        #  functionality to actually return latex... See the LatexBackend class
        if self._ref_list is not None:
            rendered_tex += bib.bib2html(self._ref_list, backend=bib.LatexBackend())

        return rendered_tex


class Tabs(NamedCompositeElement):
    """A LIVVkit Tabs element

    The Tabs element is a super element intended to logically separate elements
    into clickable tabs on the output website. It also will allow for the
    generation of other (experimental!) Report types (e.g., LaTeX), where the
    "tabs" meaning might be better interpreted as a "subsection".
    """
    _html_template = 'tabs.html'
    _latex_template = 'tabs.tex'

    def __init__(self, tabs):
        """Initialize a Tabs element

        Args:
            tabs: A dictionary where each (key, value) item represents a tab.
                Keys will become the tab text and values should be lists of
                LIVVkit elements to display within the tab
        """
        super(Tabs, self).__init__(tabs)


class Section(CompositeElement):
    """A LIVVkit Section element

    The Section element is a super element intended to logically separate elements
    into titled sections. It also will allow for the generation of other
    (experimental!) Report types (e.g., LaTeX), where the "section" meaning might
    be better interpreted as a "subsection".
    """
    _html_template = 'section.html'
    _latex_template = 'section.tex'

    def __init__(self, title, elements):
        """Initialize a Section element

        Args:
            title: The title of the section
            elements: A list of LIVVkit elements to display within the section
        """
        super(Section, self).__init__(elements)
        self.title = title


class Table(BaseElement):
    """A LIVVkit Table element

    The Table element will produce a table in the analysis report.
    """
    _html_template = 'table.html'
    _latex_template = 'table.tex'

    def __init__(self, title, data, index=False, transpose=False):
        """Initialize a Section element

                Args:
                    title: The title of the table
                    data: The data to display in the table in the form of either
                        a pandas DataFrame or a dictionary of the form
                        {column1:[row1, row2...],... } where each (key, value)
                        item is a table column, with the key being the column
                        header and the value being a list of that's columns' row
                        values.
                    index: The index to include in the table. If False, no index
                        will be included. If True, a numbered index beginning at
                        zero will be included in the table. If a collection of
                        values the same length as the data rows, the collection
                        will be used to label the rows.
                    transpose: A boolean (default: False) which will flip the
                        table (headers become the index, index becomes the header).
                """
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
    """A LIVVkit BitForBit element

    The BitForBit element will produce a table in the analysis report indicating
    bit-for-bit statuses with a difference image shown in the final column of
    the table.
    """
    _html_template = 'bit4bit.html'
    _latex_template = 'bit4bit.tex'

    def __init__(self, title, data, imgs):
        """Initialize a BitForBit element

        Args:
            title: The title of the bit-for-bit comparisons
            data: The data to display in the table in the form of either
                a pandas DataFrame or a dictionary of the form
                {column1:[row1, row2...],... } where each (key, value)
                item is a table column, with the key being the column
                header and the value being a list of that's columns' row
                values
            imgs: A list of LIVVkit Image elements to display in an additional
                final column of the bit-for-bit table. Note: The list must be
                same length as the number of rows in the table data
        """
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
    """A LIVVkit Gallery element

    The Gallery element is a super element intended to group LIVVkit Image
    elements into a gallery. It also will allow for the generation of other
    (experimental!) Report types (e.g., LaTeX), where the "Gallery" meaning
    might be better interpreted as a figure "subsection".
    """
    _html_template = 'gallery.html'
    _latex_template = 'gallery.tex'

    def __init__(self, title, elements):
        """Initialize a Gallery element

        Args:
            title: The title of the image gallery
            elements: A list of LIVVkit Image elements to display within the
                gallery
        """
        super(Gallery, self).__init__(elements)
        self.title = title


class Image(BaseElement):
    """A LIVVkit Image element

    The Image element produces an image/figure in the report.
    """
    _html_template = 'image.html'
    _latex_template = 'image.tex'

    def __init__(self, title, desc, image_file, group=None, height=None, relative_to=None):
        """Initialize a Section element

        Args:
            title: The title of the image
            desc: A description of the image which in most report forms will be
                figure caption
            image_file: The path to the image to display. Note: this should resolve
                to a path inside the report output directory
            group: Group the images into a JavaScript Lightbox with this name
                (default: None). Note: this is only relevant for an HTML report
            height: The height of the image in pixels
            relative_to: Transform the image path to be relative to this
                directory. By default, the image will assumed to be in the
                directory, or a subdirectory, of the page it's displayed on.
        """
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
    """A B4BImage element

    A dummy Image that can be used by the BitForBit element indicating a
    bit-for-bit verification result.
    """
    def __init__(self, title, description, page_path):
        """Initialize a dummy B4BImage element

        Args:
            title: The title of the image
            description: A description of the image which in most report forms
                will be figure caption
            page_path: The path to the page on which the dummy image will be
                displayed
        """
        image_file = os.path.join(livvkit.output_dir, 'imgs', 'b4b.png')

        super(B4BImage, self).__init__(title, description,
                                       image_file=image_file,
                                       relative_to=page_path,
                                       height=50, group='b4b')


class NAImage(Image):
    """A NAImage element

    A dummy Image that can be used to indicate a missing image
    """
    def __init__(self, title, description, page_path):
        """Initialize a dummy NAImage element

        Args:
            title: The title of the image
            description: A description of the image which in most report forms
                will be figure caption
            page_path: The path to the page on which the dummy image will be
                displayed
        """
        image_file = os.path.join(livvkit.output_dir, 'imgs', 'na.png')

        super(NAImage, self).__init__(title, description,
                                      image_file=image_file,
                                      relative_to=page_path,
                                      height=50, group='na')


class FileDiff(BaseElement):
    """A LIVVkit FileDiff element

    The FilleDiff element will compare two text files and produce a git-diff
    style diff of the files.
    """
    _html_template = 'diff.html'
    _latex_template = 'diff.tex'

    def __init__(self, title, from_file, to_file, context=3):
        """Initialize a FileDiff element

        Args:
            title: The title of the diff
            from_file: A path to the file which will be compared against
            to_file: A path to the file which which to compare
            context: An positive int indicating the number of lines of context
                to display on either side of each difference found
        """
        super(FileDiff, self).__init__()
        self.title = title
        self.from_file = from_file
        self.to_file = to_file
        self.diff, self.diff_status = self.diff_files(context=context)

    def diff_files(self, context=3):
        """Perform the file diff

        Args:
            context: An positive int indicating the number of lines of context
                to display on either side of each difference found

        Returns:
            (tuple): Tuple containing:
                difference: A str containing either a git-style diff of the
                    files if a difference was found or the original file in
                    full
                diff_status: A boolean indicating whether any differences were
                    found
        """
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
    """A LIVVkit Error element

    The Error element will produce an error message in the analysis report.
    """
    _html_template = 'err.html'
    _latex_template = 'err.tex'

    def __init__(self, title, message):
        """Initialize a LIVVkit Error element

        Args:
            title: The title of the error
            message: The error message to display
        """
        super(Error, self).__init__()
        self.title = title
        self.message = message


class RawHTML(BaseElement):
    """A LIVVkit RawHTML element

    The RawHTML element will directly display the contained HTML in the analysis
    report. For an HTML report (default) this will be directly written onto the
    page so is a potential security hole and should be used with caution. For the
    experimental report types (e.g., LaTeX) the contained HTML will be written to
    report in a code display block or as a raw string.
    """
    _html_template = 'raw.html'
    _latex_template = 'raw.tex'

    def __init__(self, html):
        """Initialize a LIVVkit RawHTML element

        Args:
            html: An HTML str
        """
        super(RawHTML, self).__init__()
        self.html = html
