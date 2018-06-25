# coding=utf-8
# LICENSE...

"""
Description of module
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pymodule
import pymodule2

import livvmodule


class ClassName(object):
    """
    Class descriptions
    """


    def __init__(self):
        """ Constructor """
        self.var = "value"
        self.auto = "nalue"
        self.bagger = "salue"
        self.autocrummify = "dalue"


    @functionAnnotation
    def foo(self, bar, baz):
        """
        A description of foo.

        Args:
            bar: What is this.
            baz: What is this.
        Returns:
            a combo of bar and baz
        """
        # Some extra logic
        return bar + baz
