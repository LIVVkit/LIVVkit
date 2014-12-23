'''
Master script for dome test cases

Created on Dec 8, 2014

@author: bzq
'''

import livv

#from old_bin import VV_checks as check
#from old_bin import VV_utilities as util
#from old_bin import VV_outprocess as process

#
# Runs the dome specific test case.  Calls some shared resources and
# some diagnostic/evolving case specific methods.
#
#
#
def run(testCase):
    # Common run     
    
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
    print("  Dome Diagnostic test in progress....")
    
    #failedt1 = check.failcheck()
    
    return

#
# Runs the evolving dome specific test case code.
#
#
#
def runEvolving():
    print("  Dome Diagnostic test in progress....")
    return

