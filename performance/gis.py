'''
Master module for GIS test cases.  Inherits methods from the AbstractTest
class from the Test module.  GIS specific verification are performed by calling
the run() method, which passes the necessary information to the runGisPerformance()
method.

Created on Dec 8, 2014

@author: arbennett
'''
import os

import util.variables
from base import AbstractTest
from util.parser import Parser

# Map of the options to the test cases
cases = {'none' : [],
         'dome' : [],
         'gis' : ['gis'],
         'all'  : ['gis']
        }

# Return a list of options
def choices():
    return list(cases.keys())

# Return the tests associated with an option
def choose(key):
    return cases[key] if cases.has_key(key) else None

'''
Main class for handling Greenland Ice Sheet performance validation.

The Greenland Ice Sheet test cases inherit functionality from AbstractTest for
generating scaling plots and generating the output webpage.
'''
class Test(AbstractTest):

    ''' Constructor '''
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "gis"
        self.modelDir = util.variables.performanceDir + os.sep + "gis"
        self.benchDir = util.variables.performanceDir + os.sep + "bench" + os.sep + 'gis'
        self.description = "A placeholder description"

    '''
    This method will record the specific test cases
    being run.  Each specific test case string is run via the 
    runGisPerformance function.  All of the data pulled is then
    assimilated via the runScaling method defined in the base class
    '''
    def run(self):
        print("This is a placeholder")
        return


    '''
    Greenland Ice Sheet Performance Testing
    
    @param resolution : the resolution of the test data
    '''
    def runGisPerformance(self, resolution):
        print(os.linesep + "  Greenland Ice Sheet " + resolution + " performance testing in progress....")

        # Make sure that there is some data
        if not (os.path.exists(self.modelDir) and os.path.exists(self.benchDir)):
            print("    Could not find data for GIS " + resolution + " verification!  Tried to find data in:")
            print("      " + self.modelDir)
            print("      " + self.benchDir)
            print("    Continuing with next test....")
            return

        # Process the configure files
        gisParser = Parser()
        self.modelConfigs['gis_' + resolution], self.benchConfigs['gis_' + resolution] = \
                gisParser.parseConfigurations(self.modelDir, self.benchDir)

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails['gis_' + resolution] = gisParser.parseStdOutput(self.modelDir, "^out.gis." + resolution + ".((albany)|(glissade))$")

        # Go through and pull in the timing data
        print("    Model Timing Summary:")
        self.modelTimingData['gis' + resolution] = gisParser.parseTimingSummaries(self.modelDir)
        print("    Benchmark Timing Summary:")
        self.benchTimingData['gis' + resolution] = gisParser.parseTimingSummaries(self.benchDir)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = gisParser.getParserSummary()

        self.summary['gis_' + resolution] = [numberOutputFiles, numberConfigMatches, numberConfigTests]
