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
Provides a way to check internal consistency of LIVV's capabilities.
Runs the basic verification tests for a small set of known data that
can be compared with known outputs.

Created on Dec 8, 2014

@author: arbennett
'''

import os
import shutil
import subprocess
import sys

import verification.dome
import util.variables

'''
Uses a small set of included dome data to ensure that everything in 
LIVV works as planned.
'''
def check():   
    print("Beginning internal consistency checks....")
    print("  Verifying integrity of verification tests...."),
    
    # Redirect standard output so that we don't have to see the output of these tests
    sys.stdout = open(os.devnull, "w")
    errorList = []
    dome = verification.dome.Test()
    dome.benchDir = util.variables.cwd + os.sep + "util" + os.sep + "data_base"
    
    # Compare against data that should all match
    dome.modelDir = util.variables.cwd + os.sep + "util" + os.sep + "data_same"
    dome.run()
    if not dome.bitForBitDetails["Dome 0010"]["dome.0010.p001.out.nc"][0] == 'SUCCESS':
        errorList.append("NCDiff recorded differences on results of same test.")

    # Compare against data that has a small difference
    dome.modelDir = util.variables.cwd + os.sep + "util" + os.sep + "data_diffsmall"
    dome.run()
    if not dome.bitForBitDetails["Dome 0010"]["dome.0010.p001.out.nc"][0] == 'FAILURE':
        errorList.append("NCDiff failed to record differences on small difference test") 

    # Compare against data that has a large difference
    dome.modelDir = util.variables.cwd + os.sep + "util" + os.sep + "data_difflarge"
    dome.run() 
    if not dome.bitForBitDetails["Dome 0010"]["dome.0010.p001.out.nc"][0] == 'FAILURE':
        errorList.append("NCDiff failed to record differences on small difference test") 

    # If the bit for bit difference plots are to be removed uncomment these lines
    #shutil.rmtree(util.variables.imgDir + os.sep + "Dome" + os.sep + "bit4bit")
    #os.mkdir(util.variables.imgDir + os.sep + "Dome" + os.sep + "bit4bit")
   
    # Restore standard output so that we can report and continue if possible 
    sys.stdout = sys.__stdout__
    if not errorList == []:
        # Get the current revision
        rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
        print("")
        print("")
        print("---------------------- ERROR --------------------------")
        print("  Found errors while checking internal consistency: ")
        for err in errorList:
            print("    " + err)
        print("")
        print("  Report these errors with the code " + rev + " at: ")
        print("    https://github.com/ACME-Climate/LIVV/issues")
        print("")
        print("---------------------- ERROR --------------------------")
        exit()
    else:
        print(" Okay!")
        print("")
    
    
