'''
Master script for shelf test cases

Created on Dec 8, 2014

@author: bzq
'''

#
# Runs the shelf specific test case.  Calls some shared resources and
# some circular/confined case specific methods.
#
#
#
def run(testCase):
    # Common run 
    name = testCase
    
    # Map the case names to the case functions
    callDict = {'confined-shelf' : runConfined,
                'circular-shelf' : runCircular}
    
    # Call the correct function
    callDict[testCase]()
     
    # More common postprocessing
    return
    

#
# Runs the diagnostic dome specific test case code.  
#
#
#    
def runConfined():
    print("  Confined shelf test in progress....")
    return

#
# Runs the evolving dome specific test case code.
#
#
#
def runCircular():
    print("  Circular shelf test in progress....")
    return