'''
Master script for dome test cases

Created on Dec 8, 2014

@author: bzq
'''

#
# Runs the dome specific test case.  Calls some shared resources and
# some diagnostic/evolving case specific methods.
#
#
#
def run(testCase):
    # Common run 
    name = testCase
    
    # Map the case names to the case functions
    callDict = {'dome30/diagnostic' : runDiagnostic,
                'dome30/evolving' : runEvolving}
    
    # Call the correct function
    callDict[testCase]()
     
    # More common postprocessing
    return
    

#
# Runs the diagnostic dome specific test case code.  
#
#
#    
def runDiagnostic():
    print("running dome diagnostic test")
    return

#
# Runs the evolving dome specific test case code.
#
#
#
def runEvolving():
    print("running dome evolving test")
    return