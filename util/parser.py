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
A general parser for extracting data from text files.  When using parse_configurations the
resulting dictionaries can be iterated over via the following code:

            for key1,value1 in model_configs.iteritems():
                file_name = key1
                for key2,value2 in value1.iteritems():
                    section_header = key2
                    for key3, value3 in value2.iteritems():
                        variable = key3 
                        value = value3.split("#")[0]


Created on Feb 19, 2015

@author: arbennett
"""
import os
import re
import glob
import ConfigParser
import numpy as np

import util.variables
from collections import OrderedDict


class Parser(object):
    """
    The generalized parser for processing text files associated with a test case
    
    The parser class is to be used within test classes to easily get information
    from text files.  The two main pieces of functionality of a parser are for
    reading configuration files and standard output from simulations.
    """
    def __init__(self):
        """ Constructor """
        self.config_parser = ConfigParser.ConfigParser()
        self.bench_data, self.model_data = dict(), dict()
        self.n_outputParsed = 0
        self.n_configParsed, self.n_configMatched = 0, 0

        # Build an empty ordered dictionary so that the output prints in a nice order
        self.std_out_data = OrderedDict()
        for var in util.variables.parser_vars: self.std_out_data[var] = None


    def get_parserSummary(self):
        """ Get some key details about what was parsed """
        return self.n_outputParsed, self.n_configMatched, self.n_configParsed


    def parse_configurations(self, model_dir, bench_dir, regex):
        """
        Parse through all of the configuration files from a model and benchmark
        
        Parses all of the files in the given directories and stores them as
        nested dictionaries.  The general structure of the dictionaries are
        {filename : {section_headers : {variables : values}}}.  These can be
        looped through for processing using the algorithm listed at the top 
        of this file.
        
        Args:
            model_dir: the directory for the model configuration files
            bench_dir: the directory for the benchmark configuration files
            regex: the pattern to match the config files with
        Returns:
            the nested dictionaries corresponding
                 to the files found in the input directories
        """
        # Make sure the locations exist, and if not return blank sets
        if not (os.path.exists(model_dir) and os.path.exists(bench_dir)):
            return dict(), dict()
        model_files = [fn.split(os.sep)[-1] for fn in glob.glob(model_dir + os.sep + "*" + regex)]
        bench_files = [fn.split(os.sep)[-1] for fn in glob.glob(bench_dir + os.sep + "*" + regex)]
        self.n_configParsed += len(model_files)

        # Pull in the information from the model run
        for modelF in model_files:
            model_file = model_dir + os.sep + modelF
            model_fileData = OrderedDict()
            self.config_parser.read(model_file)

            # Go through each header section (ones that look like [section])
            for section in self.config_parser.sections():
                sub_dict = OrderedDict()

                # Go through each item in the section and put {var : val} into sub_dict
                for entry in self.config_parser.items(section):
                    sub_dict[entry[0]] = entry[1].split('#')[0] 

                # Map the sub-dictionary to the section 
                model_fileData[section] = sub_dict.copy()

            # Associate the data to the file
            self.model_data[modelF] = model_fileData

        # Pull in the information from the benchmark 
        for benchF in bench_files:
            bench_file = bench_dir + os.sep + benchF
            bench_fileData = OrderedDict()
            self.config_parser.read(bench_file)

            # Go through each header section (ones that look like [section])
            for section in self.config_parser.sections():
                sub_dict = OrderedDict()

                # Go through each item in the section and put {var : val} into sub_dict
                for entry in self.config_parser.items(section):
                    sub_dict[entry[0]] = entry[1].split('#')[0] 

                # Map the sub-dictionary to the section 
                bench_fileData[section] = sub_dict.copy()

            # Associate the data with the file
            self.bench_data[benchF] = bench_fileData

        # Check to see if the files match
        # TODO: This is unwieldy - can do a better job when I'm thinking better -arbennett
        for file in model_files:
            config_matched = True
            for section, vars in self.model_data[file].iteritems():
                for var, val in self.model_data[file][section].iteritems():
                    if file in bench_files and section in self.bench_data[file] and var in self.bench_data[file][section]:
                        if val != self.bench_data[file][section][var]:
                            config_matched = False
                    else:
                        config_matched = False
            if config_matched: self.n_configMatched += 1

        return self.model_data, self.bench_data


    def parse_stdOutput(self, model_dir, regex):
        """    
        Searches through a standard output file looking key pieces of
        data about the run.  Records the dycore type, the number of 
        processors used, the average convergence rate, and number of 
        timesteps
        
        Args:
            model_dir: the directory with files to parse through
            regex: A pattern to match the std output files with
        Return:
            a mapping of the various parameters to their values from the file
        """
        # Set up variables that we can use to map data and information
        dycore_types = {"0" : "Glide", "1" : "Glam", "2" : "Glissade", "3" : "Albany_felix", "4" : "BISICLES"}
        try:
            files = os.listdir(model_dir)
        except:
            files = []
            print("    Could not find model data in" + model_dir)
        files = filter(re.compile(regex).search, files)
        outdata = []

        for file_name in files:
            # Initialize a new set of data
            number_procs = 0
            current_step = 0
            avg_itersTo_converge = 0
            iter_number = 0
            converged_iters = []
            iters_toConverge = []
            self.std_out_data = OrderedDict()

            # Open up the file
            logfile = open(model_dir + os.sep + file_name, 'r')
            self.n_outputParsed += 1

            # Go through and build up information about the simulation
            for line in logfile:
                #Determine the dycore type
                if ('CISM dycore type' in line):
                    if line.split()[-1] == '=':
                        self.std_out_data['Dycore Type'] = dycore_types[next(logfile).strip()]
                    else:
                        self.std_out_data['Dycore Type'] = dycore_types[line.split()[-1]]

                # Calculate the total number of processors used
                if ('total procs' in line):
                    number_procs += int(line.split()[-1])

                # Grab the current timestep
                if ('Nonlinear Solver Step' in line):
                    current_step = int(line.split()[4])
                if ('Compute ice velocities, time = ' in line):
                    current_step = float(line.split()[-1])

                # Get the number of iterations per timestep
                if ('"SOLVE_STATUS_CONVERGED"' in line):
                    split_line = line.split()
                    iters_toConverge.append(int(split_line[split_line.index('"SOLVE_STATUS_CONVERGED"') + 2]))

                if ("Compute dH/dt" in line):
                    iters_toConverge.append(int(iter_number))

                # If the timestep converged mark it with a positive
                if ('Converged!' in line):
                    converged_iters.append(current_step)

                # If the timestep didn't converge mark it with a negative
                if ('Failed!' in line):
                    converged_iters.append(-1*current_step)

                split_line = line.split()
                if len(split_line) > 0 and split_line[0].isdigit():
                    iter_number = split_line[0]


            # Calculate the average number of iterations it took to converge
            if (len(iters_toConverge) > 0):
                iters_toConverge.append(int(iter_number))
                current_step += 1
                avg_itersTo_converge = float(sum(iters_toConverge)) / len(iters_toConverge)

            # Record some of the data in the self.std_out_data
            self.std_out_data['Number of processors'] = number_procs
            self.std_out_data['Number of timesteps'] = int(current_step)
            if avg_itersTo_converge > 0:
                self.std_out_data['Average iterations to converge'] = avg_itersTo_converge 
            elif int(current_step) == 0:
                self.std_out_data['Number of timesteps'] = 1
                self.std_out_data['Average iterations to converge'] = iter_number

            if not self.std_out_data.has_key('Dycore Type') or self.std_out_data['Dycore Type'] == None: 
                self.std_out_data['Dycore Type'] = 'Unavailable'
            for key in self.std_out_data.keys():
                if self.std_out_data[key] == None:
                    self.std_out_data[key] = 'N/A'

            outdata.append(self.std_out_data)

        return zip(files, outdata)


    def parse_timingSummaries(self, base_path, test_name, resolution):
        """ 
        Search through gptl timing files 
        
        Args:
            base_path: the directory to look for timing files in
            test_name: the name of the test run
            resolution: a string representation of the resolution of the run
        Returns:
            a summary of the timing data that was parsed
        """
        if not os.path.exists(base_path):
            return []
        times = dict()
        timing_files = glob.glob(base_path + os.sep + "timing"+ os.sep + test_name.lower() + '-t[0-9].' + resolution + ".p[0-9][0-9][0-9].results") 
        timing_files += (glob.glob(base_path + os.sep + "timing"+ os.sep + test_name.lower() + '-t[0-9].' + resolution + ".p[0-9][0-9][0-9].cism_timing_stats") )

        for file_path in timing_files:
            run = file_path.split(os.sep)[-1].split('.')[2][1:]
            if not times.has_key(run): times[run] = []
            if not os.path.exists(file_path): continue
            
            # Open the file and grab the data outs
            file = open(file_path, 'r')
            for line in file:
                # If the line is empty just go to the next
                if line.split() == []:
                    continue
                
                # If this is a big machine this is how we find the time
                if line.split()[0] == 'cism':
                    times[run].append(float(line.split()[5]))
                    break
                
                # Otherwise it's found here
                if line.split()[0] == file_path.split(os.sep)[-1].replace('results', 'config'):
                    times[run].append(float(line.split()[1]))
            
            # Record the mean, max, and min times found
            times[run] = [np.mean(times[run]), np.max(times[run]), np.min(times[run])]
        return times
