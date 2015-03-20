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
#from bin.test import AbstractTest

#class Test(AbstractTest):
class Test():
    pass
