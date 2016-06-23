# Copyright (c) 2015, UT-BATTELLE, LLC
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
Module to hold LIVV specific data structures
"""
class LIVVDict(dict):
    """
    Extension of the dictionary datastructure to allow for auto nesting.
    """
    def __getitem__(self, item):
        """ 
        Tries to get the item, and if it's not found creates it 
        Credit to: http://tiny.cc/qerr7x 
        """
        try: 
            return dict.__getitem__(self, item)
        except KeyError:
            tmp = type(self)()
            self[item] = tmp
            return tmp

    def nested_insert(self, item_list):
        """ Create a series of nested LIVVDicts given a list """
        if len(item_list) == 1:
            self[item_list[0]] = LIVVDict()
        elif len(item_list) > 1:
            if item_list[0] not in self:
                self[item_list[0]] = LIVVDict()
            self[item_list[0]].nested_insert(item_list[1:])

    def nested_assign(self, key_list, value):
        """ Set the value of nested LIVVDicts given a list """
        if len(key_list) == 1:
            self[key_list[0]] = value
        elif len(key_list) > 1:
            if key_list[0] not in self:
                self[key_list[0]] = LIVVDict() 
            self[key_list[0]].nested_assign(key_list[1:], value)


class ElementHelper:
    """
    Helper class to make building new display elements in the output
    files easier and less error prone.  This is more useful as a 
    conceptual grouping of functions rather than a full fledged object.

    Implementing new elements is possible simply by adding new functions
    to this class.  They will be written out to the JSON files as sub-objects, 
    which must be interpreted by the Javascript found in the resources
    directory.
    """
    @staticmethod
    def section(title, description, elementList):
        """ 
        Returns a dictionary representing a new section to display elements.
        This can be thought of as a simple container for displaying multiple
        types of information.

        Args:
            title: The title to display 
            description: A description of the section
            elementList: The list of elements to display. If a single element is
                         given it will be wrapped in a list.

        Returns:
            A dictionary with metadata specifying that it is to be rendered
            as a section containing multiple elements.
        """
        sect = {}
        sect["Type"] = "Section"
        sect["Title"] = title
        sect["Description"] = description
        if type(elementList) == list:
            sect["Elements"] = elementList
        else:
            sect["Elements"] = [elementList]
        return sect

    @staticmethod
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
            data_node: A dictionary with the form:
                {"case" : {"subcase" : { "header" : "data" } } }

        Returns:
            A dictionary with the metadata specifying that it is to be
            rendered as a table.
        """
        tb = {}
        tb["Type"] = "Table"
        tb["Title"] = title
        tb["Headers"] = headers
        tb["Data"] = data_node
        return tb

    @staticmethod
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
                {"var_name" : {"header : { "data" } } }

        Returns:
            A dictionary with the metadata specifying that it is to be
            rendered as a bit for bit table
        """
        b4b = {}
        b4b["Type"] = "Bit for Bit"
        b4b["Title"] = title
        b4b["Headers"] = headers
        b4b["Data"] = data_node
        return b4b

    @staticmethod
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
        gal = {}
        gal["Type"] = "Gallery"
        gal["Title"] = title
        gal["Data"] = image_elem_list
        return gal

    @staticmethod
    def image_element(title, desc, image_name):
        """ 
        Builds an image element.  Image elements are primarily created
        and then wrapped into an image gallery element.  This is not required
        behavior, however and it's independent usage should be allowed depending
        on the behavior required.  
        
        The Javascript will search for the `image_name` in the component's 
        `imgs` directory when rendering.  For example, all verification images 
        are output to `vv_xxxx-xx-xx/verification/imgs` and then the verification 
        case's output page will search for `image_name` within that directory.

        Args:
            title: The title to display
            desc: A description of the image or plot
            image_name: The filename of the image

        Returns:
            A dictionary with the metadata specifying that it is to be
            rendered as an image element
        """
        ie = {}
        ie["Type"] = "Image"
        ie["Title"] = title
        ie["Desciption"] = desc
        ie["Plot File"] = image_name
        return ie

    @staticmethod
    def file_diff(title, diff_data):
        """ 
        Builds a file diff element.  This element can be used to check whether 
        configuration files have changed or other similar checks.  Differences
        will be highlighted when rendered via Javascript.

        Args:
            title: The title to display
            diff_data: A dictionary of the form:
                { "section_name" : { "variale_name" : [diff, val_1, val_2] } }

        Returns:
            A dictionary with the metadata specifying that it is to be 
            rendered as a file diff element
        """
        fd = {}
        fd["Type"] = "Diff"
        fd["Title"] = title
        fd["Data"] = diff_data
        return fd

    @staticmethod
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
        err = {}
        err["Type"] = "Error"
        err["Title"] = title
        err["Message"] = error_msg
        return err

