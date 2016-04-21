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

@author: arbennett
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

    def merge_leaves(self, dict_to_merge):
        """ Merges another LIVVDict's similar leaf nodes into this one """
        pass


class ElementHelper:
    """
    Helper class to make building new display elements in the output
    files easier and less error prone.  This is more useful as a 
    conceptual grouping of functions rather than a full fledged object.

    Implementing new elements is possible simply by adding new functions
    to this class.  They will be written out to the JSON files as sub-objects, 
    which must be interpreted by the Javascript which is found in the resources
    directory.
    """
    @staticmethod
    def section(title, elementList):
        """ Returns a dictionary representing a new section to display elements"""
        sect = {}
        sect["Type"] = "Section"
        sect["Title"] = title
        sect["Elements"] = elementList
        return sect

    @staticmethod
    def table(title, headers, data_node):
        """ Returns a dictionary representing a new table element """
        tb = {}
        tb["Type"] = "Table"
        tb["Title"] = title
        tb["Headers"] = headers
        tb["Data"] = data_node
        return tb

    @staticmethod
    def bit_for_bit(title, headers, data_node):
        """ Returns a dictionary representing a new bit for bit table element """
        b4b = {}
        b4b["Type"] = "Bit for Bit"
        b4b["Title"] = title
        b4b["Headers"] = headers
        b4b["Data"] = data_node
        return b4b

    @staticmethod
    def gallery(title, image_elem_list):
        """ Builds an image gallery out of a list of image elements """
        gal = {}
        gal["Type"] = "Gallery"
        gal["Title"] = title
        gal["Data"] = image_elem_list
        return gal

    @staticmethod
    def image_element(title, desc, image_path):
        """ Builds an image element """
        ie = {}
        ie["Type"] = "Image"
        ie["Title"] = title
        ie["Desciption"] = desc
        ie["Data"] = image_path
        return ie

    @staticmethod
    def diff(title, diff_data):
        """ Builds a file diff element """
        fd = {}
        fd["Type"] = "Diff"
        fd["Title"] = title
        fd["Data"] = diff_data
        return fd

    @staticmethod
    def error(title, error_msg):
        """ Builds an error element """
        err = {}
        err["Type"] = "Error"
        err["Title"] = title
        err["Message"] = error_msg
        return err

