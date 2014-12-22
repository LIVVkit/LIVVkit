'''
Master script for gis test cases

Created on Dec 8, 2014

@author: bzq
'''

#
# Runs the gis specific test case.  Calls some shared resources and
# some resolution dependent case specific methods.
#
#
#
def run(testCase):
    # Common run 
    name = testCase
    
    # Map the case names to the case functions
    callDict = {'RUN_GIS_4KM' : runSmall,
                'RUN_GIS_2KM' : runMedium,
                'RUN_GIS_1KM' : runLarge }
    
    # Call the correct function
    callDict[testCase]()
     
    # More common postprocessing
    return

#
# Runs the large gis specific test case code.  
#
#
#    
def runLarge():
    print("running large gis test.")
    return

#
# Runs the medium gis specific test case code.
#
#
#
def runMedium():
    print("running medium gis test.")
    return

#
# Runs the small gis specific test case code.
#
#
#
def runSmall():
    print("running small gis test.")
    return

