'''
Master module for GIS test cases.  Inherits methods from the AbstractTest
class from the Test module.  GIS specific verification are performed by calling
the run() method, which passes the necessary information to the runGisPerformance()
method.

Created on Dec 8, 2014

@author: arbennett
'''
from base import AbstractTest

# Map of the options to the test cases
cases = {'none' : [],
         'dome' : [],
         'gis' : ['gis'],
         'all'  : ['gis']
        }

''' Return the options for validation testing '''
def choices(): return list( cases.keys() )

''' Map the option to the test names '''
def choose(key): return cases[key] if cases.has_key(key) else None

'''
Main class for handling gis performance validation.

The dome test cases inherit functionality from AbstractTest for
generating scaling plots and generating the output webpage.
'''
class Test(AbstractTest):

    ''' Constructor '''
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "gis"
        self.description = "A placeholder description"
