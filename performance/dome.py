'''
Master module for dome performance test cases.  Inherits methods from the AbstractTest
class from the Test module.  Dome specific performance tests are performed by calling
the run() method, which passes the necessary information to the runDomePerformance()
method.

Created on Dec 8, 2014

@author: arbennett
'''
import os

from performance.base import AbstractTest
from util.parser import Parser
import util.variables

# Map of the options to the test cases
cases = {'none' : [],
         'gis' : [],
         'dome' : ['dome'],
         'all'  : ['dome']
        }

''' Return a list of options '''
def choices(): return list(cases.keys())

''' Return the tests associated with an option '''
def choose(key): return cases[key] if cases.has_key(key) else None

'''
Main class for handling dome performance validation

The dome test cases inherit functionality from AbstractTest for
generating scaling plots and generating the output webpage.
'''
class Test(AbstractTest):

    ''' Constructor '''
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "

    '''
    Runs the performance specific test cases.
    
    When running a test this call will record the specific test case
    being run.  Each specific test case string is run via the 
    runDomePerformance function.  All of the data pulled is then
    assimilated via the runScaling method defined in the base class
    '''
    def run(self):
        modelDir = util.variables.inputDir + os.sep + "dome"
        benchDir = util.variables.benchmarkDir + os.sep + "dome"
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for dome verification!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            return
        resolutions = sorted(set(fn.split('.')[1] for fn in os.listdir(modelDir)))
        for resolution in resolutions:
            self.runDome(resolution, modelDir, benchDir)
            #self.testsRun.append("Dome " + resolution)
        self.runScaling('dome', resolutions)
        self.testsRun.append('Scaling')


    '''
    Run an instance of dome performance testing
    
    @param resolution: the size of the test being analyzed
    @param perfDir: the location of the performance data
    @param perfBenchDir: the location of the benchmark performance data
    '''
    def runDome(self, resolution, perfDir, perfBenchDir):
        print("  Dome " + resolution + " performance testing in progress....")

        # Process the configure files
        domeParser = Parser()
        self.modelConfigs['Dome ' + resolution], self.benchConfigs['Dome ' + resolution] = \
                domeParser.parseConfigurations(perfDir, perfBenchDir, "*" + resolution + "*.config")

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails["Dome " + resolution] = domeParser.parseStdOutput(perfDir, "dome." + resolution + ".*.config.oe")

        # Go through and pull in the timing data
        print("    Model Timing Summary:")
        self.modelTimingData['dome' + resolution] = domeParser.parseTimingSummaries(perfDir, 'dome', resolution)
        print("    Benchmark Timing Summary:")
        self.benchTimingData['dome' + resolution] = domeParser.parseTimingSummaries(perfBenchDir, 'dome', resolution)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        self.summary['dome' + resolution] = [numberOutputFiles, numberConfigMatches, numberConfigTests]
