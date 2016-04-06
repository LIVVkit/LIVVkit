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
Executable script to start a verification and validation test suite. 
Management of the tests to be run is handled by the scheduler

@authors: arbennett, jhkennedy
"""
import os
import sys
from util import variables
variables.base_path = os.path.dirname(os.path.abspath(__file__))

def main():
    """ Direct execution. """
    from util import options, tests
    import components
    import importlib
    options.init(options.parse(sys.argv[1:]))

    print("-------------------------------------------------------------------")
    print("                      __   _____   ___   ____    _ __     ") 
    print("                     / /  /  _/ | / / | / / /__ (_) /_    ") 
    print("                    / /___/ / | |/ /| |/ /  '_// / __/    ") 
    print("                   /____/___/ |___/ |___/_/\_\/_/\__/     ")
    print("")
    print("                   Land Ice Verification & Validation     ")
    print("-------------------------------------------------------------------")
    print("  Load modules: python, ncl, nco, python_matplotlib, hdf5, netcdf,")
    print("                python_numpy, and python_netcdf4 for best results.")
    print("")
    print("  Current run: " + variables.timestamp)
    print("  User: "        + variables.user)
    print("  OS Type: "     + variables.os_type)
    print("  Machine: "     + variables.machine)
    print("  "              + variables.comment)
    
    tests.check_dependencies()
    if variables.run_tests: tests.run_tests()

    from util import scheduler, web, functions
    from util.datastructures import LIVVDict
    web.setup()
    l = [
         scheduler.run("numerics", components.numerics, variables.numerics_model_config),
         scheduler.run("verification", components.verification, variables.verification_model_config),
         scheduler.run("performance", components.performance, variables.performance_model_config),
         scheduler.run("validation", components.validation, variables.validation_model_config)
        ]
    functions.write_json({"Elements":l}, variables.output_dir, "index.json")
    scheduler.cleanup()
    
    print("-------------------------------------------------------------------")
    print(" Done!  Results can be seen in a web browser at:")
    print("        " +  variables.output_dir )
    print("-------------------------------------------------------------------")

# If called from the command line directly, go to the main method (above)
if __name__ == "__main__":
    main()

