"""
Something goes here.
"""


cases = {'none' : [],
         'small' : ['RUN_VALIDATION'],
         'large' : ['RUN_VALIDATION', 'RUN_VAL_COUPLED', 'RUN_VAL_DATA', 'RUN_VAL_YEARS', 'RUN_VAL_RANGE']}

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


#import livv
from bin.test import AbstractTest

class Test(AbstractTest):
    
    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Describe what the dome tests are all about
        self.name = "validation"
        self.description = "A good description."

    
    ## Returns the name of the test
    #
    #  output:
    #    @returns name : Dome
    #
    def getName(self):
        return self.name


    ## Runs the validation specific test case.  
    #
    #  input:
    #    @param testCase : the string indicator of the test to run
    #
    def run(self, testCase):
        pass



