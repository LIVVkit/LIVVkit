#!/usr/bin/env python

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
"""
Executable script to start a verification and validation test suite.  This script
handles options and setting up data storage from the options.  Each of the 
sub-categories (verification, performance, validation, and numerics) are launched
using their respective schedulers found in their subdirectories.

Created on Dec 3, 2014

@authors: arbennett, jhkennedy
"""
import os
import sys

import util.variables

util.variables.base_path = os.path.dirname(os.path.abspath(__file__))

"""
Direct execution.
"""
def main():

    import util.options
    import util.dependencies

    util.options.init(util.options.parse(sys.argv[1:]))
    print("------------------------------------------------------------------------------")
    print("                          __   _____   ___   ____    _ __     ") 
    print("                         / /  /  _/ | / / | / / /__ (_) /_    ") 
    print("                        / /___/ / | |/ /| |/ /  '_// / __/    ") 
    print("                       /____/___/ |___/ |___/_/\_\/_/\__/     ")
    print("")
    print("                       Land Ice Verification & Validation     ")
    print("------------------------------------------------------------------------------")
    print("  Load modules: python, ncl, nco, python_matplotlib, hdf5, netcdf,")
    print("                python_numpy, and python_netcdf4 for best results.")
    print("")
    print("  Current run: " + util.variables.timestamp)
    print("  User: " + util.variables.user)
    print("  OS Type: " + util.variables.os_type)
    print("  Machine: " + util.variables.machine)
    print("  " + util.variables.comment)
    
    util.dependencies.check()
   
    import util.scheduler
    import util.web

    util.web.setup()
    
    util.scheduler.run_numerics()
    util.scheduler.run_verification()
    util.scheduler.run_performance()
    util.scheduler.run_validation()

    util.scheduler.cleanup()
    
    print("------------------------------------------------------------------------------")
    print("Finished running LIVV.")
    print("  Open " + util.variables.output_dir + "/index.html to see test results")
    print("------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()

