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
    callDict = {'ismip-hom-a/20km' : runLargeA,
                'ismip-hom-c/20km' : runLargeC,
                'ismip-hom-a/80km' : runSmallA,
                'ismip-hom-c/80km' : runSmallC }
    
    # Call the correct function
    callDict[testCase]()
     
    # More common postprocessing
    return

#
# Runs the diagnostic dome specific test case code.  
#
#
#    
def runLargeA():
    print("  Large ismip-hom-a test in progress....")
    return

#
# Runs the evolving dome specific test case code.
#
#
#
def runLargeC():
    print("  Large ismip-hom-c test in progress....")
    return

#
# Runs the evolving dome specific test case code.
#
#
#
def runSmallA():
    print("  Small ismip-hom-a test in progress....")
    return

#
# Runs the evolving dome specific test case code.
#
#
#
def runSmallC():
    print("  Small ismip-hom-c test in progress....")
    return
