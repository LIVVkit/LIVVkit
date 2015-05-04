'''
Master module for GIS test cases.  Inherits methods from the AbstractTest
class from the Test module.  GIS specific verification are performed by calling
the run() method, which passes the necessary information to the runGisPerformance()
method.

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import glob
import subprocess
import itertools

# Map of the options to the test cases
cases = {'none' : [],
         'dome' : [],
         'gis' : ['gis'],
         'all'  : ['gis']
        }

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key] if cases.has_key(key) else None

from base import AbstractTest
from util.parser import Parser

## Main class for handling gis performance validation.
#
#  The dome test cases inherit functionality from AbstractTest for
#  generating scaling plots and generating the output webpage.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Describe what the dome verification are all about
        self.name = "gis"
        self.description = "A placeholder description"
