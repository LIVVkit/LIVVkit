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
The scheduler for the validation tests.  It will handle the entire 
lifecycle of any validation tests and associated files/processes.
Should be used in the following order:
    setup -> schedule -> run -> cleanup

@author arbennett
"""
import os
import importlib
import pprint

import util.variables
import validation.validation_utils.ValidationParser as ValidationParser

class ValidationScheduler(object):

    def __init__(self):
        """ Constructor """
        self.output_dir = util.variables.index_dir + os.sep + "validation"
        self.validations = dict() 
        self.summary = dict()


    def setup(self):
        """
        Prepare information for running validation tests.  This will
        need to make sure the directory structure is correct, read
        configuration files, and do some other checking to make sure
        that we are safe to run.
        """
        print("--------------------------------------------------------------------------")
        print("  Beginning validation test suite....")
        print("--------------------------------------------------------------------------")
        validation_parser = ValidationParser.ValidationParser()
        for config in util.variables.validation:
            self.validations[config] = validation_parser.read_dict(config)
        util.variables.validations = self.validations.keys()
       
        # Set up directories for output\
        for val in util.variables.validations:
            util.websetup.mkdir_p(self.output_dir)

    def schedule(self):
        """ Make the validation run efficiently. """
        for conf, vals in self.validations.items():
            for test_name, test_params in vals.items():
                print("    " + test_name.capitalize() + " in progress...")
                util.websetup.mkdir_p(self.output_dir + os.sep + test_name + os.sep + 'imgs')
                m = importlib.import_module(test_params['module'])
                val = m.Test()
                val.name = test_name
                val.run(**test_params)
                val.generate()
                self.summary[val.name] = val.summary


    def run(self):
        """ Make the magic happen. """
        return
    
    
    def cleanup(self):
        """ And finally, take care of the mess we've made. """
        return
    
    
    
