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

from __future__ import absolute_import, division, print_function, unicode_literals


class LIVVDict(dict):
    """
    Extension of the dictionary data structure to allow for auto nesting.
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
