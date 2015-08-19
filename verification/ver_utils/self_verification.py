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
import Queue
import verification.dome
import util.variables


def check():   
    '''
    Uses a small set of included dome data to ensure that everything in 
    LIVV works as planned.
    '''
    print("Beginning internal consistency checks....")
    print("  Verifying integrity of verification tests...."),
    
    # Redirect standard output so that we don't have to see the output of these tests
    #sys.stdout = open(os.devnull, "w")
    error_list = []
    fake_summary = dict()
    dome = verification.dome.Test()
    dome.bench_dir = util.variables.cwd + os.sep + "util" + os.sep + "data_base"
    
    # Compare against data that should all match
    dome.model_dir = util.variables.cwd + os.sep + "util" + os.sep + "data_same"
    dome.run(fake_summary, Queue.Queue())
    if not dome.bit_for_bit_details["Dome 0010"]["dome.0010.p001.out.nc"][0] == 'SUCCESS':
        error_list.append("NCDiff recorded differences on results of same test.")

    # Compare against data that has a small difference
    dome.model_dir = util.variables.cwd + os.sep + "util" + os.sep + "data_diffsmall"
    dome.run(fake_summary, Queue.Queue())
    if not dome.bit_for_bit_details["Dome 0010"]["dome.0010.p001.out.nc"][0] == 'FAILURE':
        error_list.append("NCDiff failed to record differences on small difference test") 

    # Compare against data that has a large difference
    dome.model_dir = util.variables.cwd + os.sep + "util" + os.sep + "data_difflarge"
    dome.run(fake_summary, Queue.Queue()) 
    if not dome.bit_for_bit_details["Dome 0010"]["dome.0010.p001.out.nc"][0] == 'FAILURE':
        error_list.append("NCDiff failed to record differences on small difference test") 

    # If the bit for bit difference plots are to be removed uncomment these lines
    #shutil.rmtree(util.variables.img_dir + os.sep + "Dome" + os.sep + "bit4bit")
    #os.mkdir(util.variables.img_dir + os.sep + "Dome" + os.sep + "bit4bit")
   
    # Restore standard output so that we can report and continue if possible 
    #sys.stdout = sys.__stdout__
    if not error_list == []:
        # Get the current revision
        rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
        print("")
        print("")
        print("---------------------- ERROR --------------------------")
        print("  Found errors while checking internal consistency: ")
        for err in error_list:
            print("    " + err)
        print("")
        print("  Report these errors with the code " + rev + " at: ")
        print("    https://github.com/LIVVkit/LIVVkit/issues")
        print("")
        print("---------------------- ERROR --------------------------")
        exit()
    else:
        print(" Okay!")
        print("")
