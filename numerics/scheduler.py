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
Scheduler for the numerics package.

@author arbennett
"""
import os
import glob
import importlib
import Queue
import time
import multiprocessing
from threading import Thread

import util.variables
import util.websetup
import numerics.ismip

class NumericsScheduler(object):

    def __init__(self):
        """ Constructor """
        self.manager = None
        self.output = None
        self.process_handles = None
        self.summary = None


    def setup(self):
        """
        Prepare information for running numerics tests.  This will
        need to make sure the directory structure is correct, read
        configuration files, and do some other checking to make sure
        that we are safe to run.
        """
        print("--------------------------------------------------------------------------")
        print("  Beginning numerics test suite....")
        print("--------------------------------------------------------------------------")
        # Make sure that the directory structure is okay
        if not os.path.exists(util.variables.input_dir):
            print("ERROR: Could not find " + util.variables.input_dir + " for input")
            print("       Use the -t and -b flags to specify the locations of the test and benchmark data.")
            print("       See README.md for more details.")
            print("------------------------------------------------------------------------------")
            exit(1)       

        # Numerics tests we run
        util.variables.numerics = [
                        numerics.ismip
                        ]

        # Set up directories for output\
        for ver in util.variables.numerics:
            test_dir = util.variables.index_dir + os.sep + "numerics" + os.sep + ver.get_name().capitalize()
            util.websetup.mkdir_p(test_dir)
            util.websetup.mkdir_p(test_dir + os.sep + "imgs")
    
    
    def schedule(self):
        """ 
        Creates a process handle for each of the numerics tests
        to be run.
        """
        self.manager = multiprocessing.Manager()
        self.output = self.manager.Queue()
        self.summary = self.manager.dict()
        self.process_handles = [multiprocessing.Process(target=num_type.Test().run, 
                                                          args=(self.summary, self.output)) 
                                  for num_type in util.variables.numerics]
    
    def run(self):
        """ 
        Launches all of the processes and synchronizes their output. 
        """
        # Spawn a new process for each test
        for p in self.process_handles:
            p.start()
        
        for p in self.process_handles:
            p.join()

        # Show the results
        while self.output.qsize() > 0:
            print self.output.get()
        
    
    def cleanup(self):
        """ And finally, take care of the mess we've made. """
        for sub_dir in os.listdir(util.variables.input_dir):
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "temp.*")]
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "*.tmp")]
        for sub_dir in os.listdir(util.variables.benchmark_dir):
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "temp.*")]
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "*.tmp")]
        return
    
