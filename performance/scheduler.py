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
The scheduler for the performance tests.  It will handle the entire 
lifecycle of any verification tests and associated files/processes.
Should be used in the following order:
    setup -> schedule -> run -> cleanup

@author arbennett
"""
import os
import glob
import importlib
import multiprocessing

import util.variables
import util.websetup
import performance.dome

class PerformanceScheduler(object):

    def __init__(self):
        """ Constructor """
        self.manager = None
        self.output = None
        self.process_handles = None
        self.summary = None


    def setup(self):
        """
        Prepare information for running verification tests.  This will
        need to make sure the directory structure is correct, read
        configuration files, and do some other checking to make sure
        that we are safe to run.
        """
        print("--------------------------------------------------------------------------")
        print("  Beginning performance test suite....")
        print("--------------------------------------------------------------------------")
        # Make sure that the directory structure is okay
        for data_dir in [util.variables.input_dir, util.variables.benchmark_dir]:
            if not os.path.exists(data_dir):
                print("ERROR: Could not find " + data_dir + " for input")
                print("       Use the -t and -b flags to specify the locations of the test and benchmark data.")
                print("       See README.md for more details.")
                print("------------------------------------------------------------------------------")
                exit(1)       

        # Verification tests we run
        util.variables.performance = [
                         performance.dome, 
                        ]
        
        # Set up directories for output\
        for ver in util.variables.performance:
            test_dir = util.variables.index_dir + os.sep + "performance" + os.sep + ver.get_name().capitalize()
            util.websetup.mkdir_p(test_dir)
            util.websetup.mkdir_p(test_dir + os.sep + "imgs")

    
    
    def schedule(self):
        """ 
        Creates a process handle for each of the performance tests
        to be run.
        """
        self.manager = multiprocessing.Manager()
        self.output = multiprocessing.Queue()
        self.summary = self.manager.dict()
        self.process_handles = [multiprocessing.Process(target=perf_type.Test().run, 
                                                          args=(self.summary, self.output)) 
                                  for perf_type in util.variables.performance]
    
    
    def run(self):
        """ 
        Launches all of the processes and synchronizes their output. 
        """
        # Spawn a new process for each test
        for p in self.process_handles:
            p.start()
            p.join()
        
        # Wait for all of the tests to finish
        while len(multiprocessing.active_children()) > len(util.variables.performance):
            time.sleep(0.25)
      
        # Show the results
        while self.output.qsize() > 0:
            print(self.output.get())
    
    
    def cleanup(self):
        """ And finally, take care of the mess we've made. """
        for sub_dir in os.listdir(util.variables.input_dir):
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "temp.*")]
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "*.tmp")]
        for sub_dir in os.listdir(util.variables.benchmark_dir):
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "temp.*")]
            [os.remove(temp_file) for temp_file in glob.glob(util.variables.input_dir + os.sep + sub_dir + os.sep + "*.tmp")]
        return
    
    
 
