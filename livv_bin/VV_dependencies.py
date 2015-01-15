'''
Dependency management for LIVV

Created on January 6, 2015

@author: bzq
'''


import os
import sys

#
# Run all of the checks for dependencies required by LIVV
#
#
def check():
    # Create a list to store all of the errors that were found
    depErrors = []
    
    print("")
    print("Beginning Dependency Checks........"),
    
    # Make sure all environment variables are set
    if os.environ.get('NCARG_ROOT') == None:
        depErrors.append("  NCARG_ROOT not found in environment")
        
    # Make sure all imports are going to work
    modules = ["jinja2"]
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            depErrors.append("  Could not Import " + module)
        
    # Show all of the dependency errors that were found
    if len(depErrors) > 0:
        print("Uh oh!")
        print("")
        print("Errors checking dependencies.  Errors found: ")
        for err in depErrors: print(err)
        exit(len(depErrors))
    else:
        print("Okay!")