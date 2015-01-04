'''
Contains the specifications for how to handle preconfigured machine options.  

Created on Dec 23, 2014

@author: bzq
'''

import os
import livv

#
# Load a configuration file from the configurations directory at the root
# of LIVV.
#
# Input:
#    machineName: the name of the file to load from
#
def load(machineName):
    # Tell the user where we are going to load from
    configFile = livv.cwd + os.sep + "configurations" + os.sep + machineName
    print("Loading configuration file from " + configFile )\
    
    # Load up the file
    try:
        execfile(configFile )
    except Exception as e:
        print(e)
        exit()
    
    # Return all of the local variables, including what was read in
    return locals()

#
# Write a configuration file to the configurations directory at the root
# of LIVV.
#
# Input:
#    machineName: the name of the file to write to
#
def save(machineName):

    # Pull in the variables needed and tell user where they'll go 
    from livv import *
    configFile = livv.cwd + os.sep + "configurations" + os.sep + machineName
    print("Saving configuration to " + configFile )
    
    # Open the file for writing
    f = open(configFile, 'w')
    f.write("# Import variables for running livv on " + machineName +"\n")
    
    # Iterate over all of the variables and only write out string variables
    # this avoids writing out objects, and also writes a complete set of info
    for k, v in locals().iteritems():
        if type(v) == type(''):
            f.write(str(k) + " = \'" + str(v) + "\'\n")
    
    # Close the output file
    f.close()
    return
    