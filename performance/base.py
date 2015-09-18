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
Performance Testing Base Module.  Defines the AbstractTest class is 
inherited by all performance test classes.

Created on Apr 21, 2015

@author: arbennett
"""
import os
import glob
import jinja2
from abc import ABCMeta, abstractmethod
from collections import Counter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

import util.variables

class AbstractTest(object):
    """
    AbstractTest provides base functionality for a performance test
    
    Each test within LIVV needs to be able to run specific test code, and
    generate its output.  Tests inherit a common method of generating 
    scaling plots
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ Constructor for the abstract base of performance tests. """
        self.name = "n/a"    # A name for the test
        self.tests_run = []    # A list of the test cases run
        self.summary = dict() # Used to store some key indicators 
        self.plot_details = dict()    # Summary of plots generated
        self.model_details = dict()    # Stats parsed from std out files for the model run
        self.bench_details = dict()    # Stats parsed from std out files for the benchmarks
        self.model_dir, self.bench_dir = "", "" # Paths to the model and benchmark data
        self.model_configs, self.bench_configs = dict(), dict()    # Summaries of the config files parsed
        self.model_timing_data, self.bench_timing_data = dict(), dict()    # Summaries of the timing data parsed


    @abstractmethod
    def run(self, summary, output):
        """
        Definition for the general test run
        
        Args:
            test_type -- The name of the test sub-test_type being run
        """
        pass


    def run_scaling(self, test_type, resolutions, output):
        """
        Generates scaling plots for each variable and dycore combination of a given
        test_type.
    
        Args:
            test_type: the overarching test category to generate scaling plots for (ie dome/gis)
            resolutions: a list of the resolutions the model was run at
        """
        self.images_generated = []
        output.put(os.linesep + "  Generating scaling plots for " + test_type + "....")

        self.weak_scaling(test_type, resolutions)
        self.strong_scaling(test_type, resolutions)

        # Record the plots
        self.plot_details['Scaling'] = self.images_generated


    def weak_scaling(self, test_type, resolutions):
        """
        Generates a weak scaling plot.  This function is greedy, it will
        find the most data points to plot from the data it is given.
        
        Args:
            test_type: the overarching test category to generate scaling plots for (ie dome/gis)
            resolutions: a list of the resolutions the model was run at
        """
        work_perProc, plot_vars = [], []
        resolutions = sorted(resolutions)
        # Find out how much work per processor for each run
        for res in resolutions:
            test = test_type + res
            proc_list = self.model_timing_data[test].keys()
            work_perProc.append([(int(res)**2)/int(n_proc)for n_proc in proc_list])

        # To generate the best plot, figure out which work/processor number 
        # was most common, then pull out the resolution, number of processor,
        # and the time taken 
        work_perProc = [i for sublist in work_perProc for i in sublist]
        
        # If there's no data quit early
        if work_perProc == []:
            return
       
        # This gets the most applicable data points to plot
        scaling_constant = Counter(work_perProc).most_common()[0][0]
        for res in resolutions: 
            test= test_type + res
            proc_list = self.model_timing_data[test].keys()
            for n_proc in proc_list:
                if (int(res)**2)/int(n_proc) == scaling_constant:
                    plot_vars.append([res, n_proc, self.model_timing_data[test_type + res][n_proc]["Run Time"]])  
        
        # These are the plotting variables
        resolutions = [int(var[0]) for var in plot_vars]
        processors = [int(var[1]) for var in plot_vars]
        times = [var[2] for var in plot_vars]
        mins = [var[-1] for var in times]
        maxs = [var[1] for var in times]
        times = [var[0] for var in times]
        # Plot it and then save the file + record it so we can link to it
        fig, ax = pyplot.subplots(1)
        pyplot.title("Weak scaling for " + test_type)
        pyplot.xlabel("Problem size")
        pyplot.ylabel("Time (s)")
        pyplot.xticks()
        pyplot.yticks()
        ax.plot(resolutions, times, 'bo-', label='Model')
        ax.plot(resolutions, mins, 'b--')
        ax.plot(resolutions, maxs, 'b--')
        #print("Saving plot to " + util.variables.img_dir + os.sep + self.name.capitalize() + os.sep + test_type +  "_scaling_weak.png")
        pyplot.savefig(util.variables.index_dir + os.sep + "performance" + os.sep + self.name + os.sep + "imgs" + os.sep + test_type.strip() +  "_scaling_weak.png")
        self.images_generated.append( [test_type.strip() + "_scaling_weak.png", "Weak scaling for " + test_type])


    def strong_scaling(self, test_type, resolutions):
        """
        Generates strong scaling plots for each of the resolutions
        that the model was run at.  
        
        Args:
            test_type: the overarching test category to generate scaling plots for (ie dome/gis)
            resolutions: a list of the resolutions the model was run at
        """
        # Generate all of the plots
        for res in sorted(resolutions):
            test = test_type + res
            # Add the data if it's available and has at least 3 data points
            if self.model_timing_data[test] != {} and len(self.model_timing_data[test].keys()) > 2:                
                model_data = self.model_timing_data[test]
                fig, ax = pyplot.subplots(1)
                pyplot.title("Strong scaling for " + test_type  + res)
                pyplot.xlabel("Number of processors")
                pyplot.ylabel("Time (s)")
                pyplot.xticks()
                pyplot.yticks()
                x = sorted(model_data.keys())
                times = [model_data[p]["Run Time"] for p in x] 
                y, mins, maxs = [], [], []
                for time in times:
                    y.append(time[0])
                    mins.append(time[1])
                    maxs.append(time[2])

                ax.plot(x, y, 'bo-', label='Model')
                ax.plot(x,mins, 'b--')
                ax.plot(x,maxs, 'b--')
                
                # Add benchmark data if it's there
                if self.bench_timing_data[test] != {}:
                    bench_data = self.bench_timing_data[test]
                    x = sorted(bench_data.keys())
                    times = [bench_data[p]["Run Time"] for p in x] 
                    y, mins, maxs = [], [], []
                    for time in times:
                        y.append(time[0])
                        mins.append(time[1])
                        maxs.append(time[2])
                    ax.plot(x, y, 'r^-', label='Benchmark')
                    ax.plot(x,mins, 'r--')
                    ax.plot(x,maxs, 'r--')
                    pyplot.legend()

                pyplot.savefig(util.variables.index_dir + os.sep + "performance" + os.sep + self.name + os.sep + "imgs" + os.sep + test_type.strip() + "_" + res +  "_scaling" + ".png")
                self.images_generated.append( [test_type.strip() + "_" + res + "_scaling" + ".png", "Strong scaling for " + test_type + res])


    def generate(self):
        """
        Create a {{test}}.html page in the output directory.
        This page will contain a detailed list of the results from LIVV.  Details
        from the run are pulled from two locations.  Global definitions that are 
        displayed on every page, or used for navigation purposes are imported
        from the main livv.py module.  All test specific information is supplied
        via class variables.
        
        @note Paths that are contained in template_vars should not be using os.sep
              since they are for html.
        """
        # Set up jinja related variables
        template_loader = jinja2.FileSystemLoader(searchpath=util.variables.template_dir)
        template_env = jinja2.Environment(loader=template_loader, extensions=["jinja2.ext.do",])
        template_file = "/performance_test.html"
        template = template_env.get_template(template_file)

        # Set up relative paths
        index_dir = ".."
        css_dir = index_dir + "/css"
        img_dir = index_dir + "/imgs"
        test_imgDir = index_dir + "/performance/" + self.name.capitalize() + "/imgs" 

        # Grab all of our images
        test_images = [os.path.basename(img) for img in glob.glob(test_imgDir + os.sep + "*.png")]
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + os.sep +"*.jpg")])
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + os.sep +"*.svg")])

        # Set up the template variables  
        template_vars = {"timestamp" : util.variables.timestamp,
                        "user" : util.variables.user,
                        "comment" : util.variables.comment,
                        "test_name" : self.name,
                        "index_dir" : index_dir,
                        "css_dir" : css_dir,
                        "img_dir" : img_dir,
                        "test_imgDir" : test_imgDir,
                        "test_description" : self.description,
                        "tests_run" : self.tests_run,
                        "test_header" : util.variables.parser_vars,
                        "test_details" : self.model_details,
                        "bench_details" : self.bench_details,
                        "plot_details" : self.plot_details,
                        "model_configs" : self.model_configs,
                        "bench_configs" : self.bench_configs,
                        "model_timing_data" : self.model_timing_data,
                        "bench_timing_data" : self.bench_timing_data,
                        "test_images" : test_images}
        output_text = template.render( template_vars )
        page = open(util.variables.index_dir + os.sep + "performance" + os.sep + self.name.lower() + '.html', "w")
        page.write(output_text)
        page.close()
