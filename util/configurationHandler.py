# Copyright (c) 2015, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


'''
Contains the specifications for how to handle preconfigured machine options

Created on Dec 23, 2014

@author: arbennett
'''

import os
import util.variables
from util.variables import *

'''
Load a configuration file from the configurations directory at the root of LIVV.

@param machineName: the name of the file to load from
@returns locals: The list of variables loaded from the file
'''
def load(machineName):
    # Tell the user where we are going to load from
    configFile = util.variables.cwd + os.sep + "configurations" + os.sep + machineName
    print("Loading configuration file from " + configFile )

    # Load up the file
    try:
        execfile(configFile)
    except Exception as e:
        print(e)
        exit()

    # Return all of the local variables, including what was read in
    return locals()


'''
Write a configuration file to the configurations directory at the root of LIVV.

@param machineName: the name of the file to write to
'''
def save(machineName):
    # Pull in the variables needed and tell user where they'll go 
    configFile = util.variables.cwd + os.sep + "configurations" + os.sep + machineName
    from util.variables import *
    print("Saving configuration to " + configFile )

    f = open(configFile, 'w')
    f.write("# Import variables for running livv on " + machineName +"\n")

    # Iterate over all of the variables and only write out string variables
    # this avoids writing out objects, and also writes a complete set of info
    for k, v in locals().iteritems():
        if type(v) == type(''):
            f.write(str(k) + " = \'" + str(v) + "\'\n")
    f.close()
