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
Performance Test Base Module.  

@author: arbennett
"""

import os
import glob
import json
import util.variables
import util.datastructures

from util.datastructures import LIVVDict

def run_suite(case, config, summary):
    """ Run the full suite of performance tests """
    result = LIVVDict()
    result[case] = LIVVDict()
    model_dir = os.path.join(util.variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(util.variables.bench_dir, config['data_dir'], case)
    model_cases = []
    bench_cases = []

    for data_dir, cases in zip([model_dir, bench_dir], [model_cases, bench_cases]):
        for root, dirs, files in os.walk(data_dir):
            if not dirs:
                cases.append(root.strip(data_dir).split(os.sep))
   
    model_cases = sorted(model_cases)
    for mcase in model_cases:
        bench_path = (os.path.join(bench_dir, os.sep.join(mcase))
                        if mcase in bench_cases else None)
        model_path = os.path.join(model_dir, os.sep.join(mcase))
        result[case].nested_assign(mcase, analyze_case(model_path, bench_path, config))
    
    print_result(case,result) #TODO
    write_result(case,result) 
    summarize_result(case, result, summary) #TODO

def analyze_case(model_dir, bench_dir, config):
    """ Run all of the performance checks on a particular case """
    result = LIVVDict()
    model_timings = set([os.path.basename(f) for f in 
                        glob.glob(os.path.join(model_dir, "*" + config["timing_ext"]))])

    if bench_dir is not None:
        bench_timings = set([os.path.basename(f) for f in 
                          glob.glob(os.path.join(model_dir, "*" + config["timing_ext"]))])
    else:
        bench_timings = set()
    
    for mtf in model_timings:
        result["model"][mtf] = parse_gptl(os.path.join(model_dir,mtf), 
                                           config["timing_vars"])
        if mtf in bench_timings: 
            result["bench"][mtf] = parse_gptl(os.path.join(bench_dir,mtf),
                                               config["timing_vars"])
    return result

def weak_scaling():
    """ Generate weak scaling stats """
    #work_perProc, plot_vars = [], []
    #resolutions = sorted(resolutions)
    ## Find out how much work per processor for each run
    #for res in resolutions:
    #    test = test_type + res
    #    proc_list = self.model_timing_data[test].keys()
    #    work_perProc.append([(int(res)**2)/int(n_proc)for n_proc in proc_list])

    ## To generate the best plot, figure out which work/processor number 
    ## was most common, then pull out the resolution, number of processor,
    ## and the time taken 
    #work_perProc = [i for sublist in work_perProc for i in sublist]
    #
    ## If there's no data quit early
    #if work_perProc == []:
    #    return
    #
    ## This gets the most applicable data points to plot
    #scaling_constant = Counter(work_perProc).most_common()[0][0]
    #for res in resolutions: 
    #    test= test_type + res
    #    proc_list = self.model_timing_data[test].keys()
    #    for n_proc in proc_list:
    #        if (int(res)**2)/int(n_proc) == scaling_constant:
    #            plot_vars.append([res, n_proc, 
    #                self.model_timing_data[test_type + res][n_proc]["Run Time"]])  
    #
    ## These are the plotting variables
    #resolutions = [int(var[0]) for var in plot_vars]
    #processors = [int(var[1]) for var in plot_vars]
    #times = [var[2] for var in plot_vars]
    #mins = [var[-1] for var in times]
    #maxs = [var[1] for var in times]
    #times = [var[0] for var in times]
    ## Plot it and then save the file + record it so we can link to it
    #fig, ax = pyplot.subplots(1)
    #pyplot.title("Weak scaling for " + test_type)
    #pyplot.xlabel("Problem size")
    #pyplot.ylabel("Time (s)")
    #pyplot.xticks()
    #pyplot.yticks()
    #ax.plot(resolutions, times, 'bo-', label='Model')
    #ax.plot(resolutions, mins, 'b--')
    #ax.plot(resolutions, maxs, 'b--')
    #pyplot.savefig(util.variables.index_dir + os.sep + "performance" + 
    #               os.sep + self.name + os.sep + "imgs" + os.sep + 
    #               test_type.strip() +  "_scaling_weak.png")
    #self.images_generated.append( [test_type.strip() + "_scaling_weak.png", 
    #                              "Weak scaling for " + test_type])


def strong_scaling():
    """ Generate strong scaling stats """
    ## Generate all of the plots
    #for res in sorted(resolutions):
    #    test = test_type + res
    #    # Add the data if it's available and has at least 3 data points
    #    if self.model_timing_data[test] != {} and len(self.model_timing_data[test].keys()) > 2:
    #        model_data = self.model_timing_data[test]
    #        fig, ax = pyplot.subplots(1)
    #        pyplot.title("Strong scaling for " + test_type  + res)
    #        pyplot.xlabel("Number of processors")
    #        pyplot.ylabel("Time (s)")
    #        pyplot.xticks()
    #        pyplot.yticks()
    #        x = sorted(model_data.keys())
    #        times = [model_data[p]["Run Time"] for p in x] 
    #        y, mins, maxs = [], [], []
    #        for time in times:
    #            y.append(time[0])
    #            mins.append(time[1])
    #            maxs.append(time[2])

    #        ax.plot(x, y, 'bo-', label='Model')
    #        ax.plot(x,mins, 'b--')
    #        ax.plot(x,maxs, 'b--')
    #        
    #        # Add benchmark data if it's there
    #        if self.bench_timing_data[test] != {}:
    #            bench_data = self.bench_timing_data[test]
    #            x = sorted(bench_data.keys())
    #            times = [bench_data[p]["Run Time"] for p in x] 
    #            y, mins, maxs = [], [], []
    #            for time in times:
    #                y.append(time[0])
    #                mins.append(time[1])
    #                maxs.append(time[2])
    #            ax.plot(x, y, 'r^-', label='Benchmark')
    #            ax.plot(x,mins, 'r--')
    #            ax.plot(x,maxs, 'r--')
    #            pyplot.legend()

    #        pyplot.savefig(util.variables.index_dir + os.sep + "performance" + 
    #                       os.sep + self.name + os.sep + "imgs" + os.sep + 
    #                       test_type.strip() + "_" + res +  "_scaling" + ".png")
    #        self.images_generated.append( [test_type.strip() + "_" + res + "_scaling" + 
    #                                       ".png", "Strong scaling for " + test_type + res])



def generate_timing_stats(model_dir, bench_dir, config):
    """
    Parse all of the timing files, and generate some statistics
    about the run.

    Args:
        model_dir: Path to the model output
        bench_dir: Path to the benchmark data
        config: A dictionary containing option specifications

    Returns:
        A LIVVDict containing values that have the form: 
            [mean, min, max, mean, diff. from bench mean]
    """
    timing_result = LIVVDict()
    # TODO
    return timing_result


def parse_gptl(file_path, var_list):
    """
    Read a GPTL timing file and extract some data.

    Args:
        file_path: the path to the GPTL timing file
        var_list: a list of strings to look for in the file

    Returns:
        A LIVVDict containing key-value pairs of the variables
        and the times associated with them
    """
    timing_result = LIVVDict()
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            for var in var_list:
                for line in f:
                    if var in line:
                        timing_result[var] = float(line.split()[4])/int(line.split()[2])
    return timing_result


def print_result(case,result):
    """ Show some statistics from the run """
    pass


def write_result(case,result):
    """ Take the result and write out a JSON file """
    outpath = os.path.join(util.variables.output_dir, "Performance", case)
    util.datastructures.mkdir_p(outpath)
    with open(os.path.join(outpath, case+".json"), 'w') as f:
        json.dump(result, f, indent=4)

def summarize_result(case, result, summary):
    """ Trim out some data to return for the index page """
    # Get the number of bit for bit failures
    # Get the number of config matches
    # Get the number of files parsed

