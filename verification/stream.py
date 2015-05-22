'''
Master module for stream test cases.  Inherits methods from the AbstractTest
class from the base module.  Stream specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the runStream()
method.

Created on May 6, 2015

@author: arbennett
'''
import os
import fnmatch

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

'''
Main class for handling stream test cases.

The stream test cases inherit functionality from AbstractTest for checking 
bit-for-bittedness from a model run. This class handles evolving and \
diagnostic variations of the stream case.
'''
class Test(AbstractTest):

    ''' Constructor '''
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "Stream"
        self.modelDir = util.variables.inputDir + os.sep + "stream"
        self.benchDir = util.variables.benchmarkDir + os.sep + "stream"
        self.description = "Description of stream"


    '''
    Runs all of the available stream tests.  Looks in the model and
    benchmark directories for different variations, and then runs
    the runStream() method with the correct information
    '''
    def run(self):
        if not (os.path.exists(self.modelDir) and os.path.exists(self.benchDir)):
            print("    Could not find data for stream  verification!  Tried to find data in:")
            print("      " + self.modelDir)
            print("      " + self.benchDir)
            print("    Continuing with next test....")
            return

        resolutions = set()
        modelConfigFiles = fnmatch.filter(os.listdir(self.modelDir), 'stream*.config')
        for mcf in modelConfigFiles:
            resolutions.add( mcf.split('.')[1] )
        resolutions = sorted( resolutions )
                
        self.runStream(resolutions[0], self.modelDir, self.benchDir)
        self.testsRun.append("Stream " + resolutions[0])


    '''
    Runs the stream V&V for a given resolution.  First parses through all 
    of the standard output & config files for the given test case, then finishes up by 
    doing bit for bit comparisons with the benchmark files.
    
    @param resolution: The resolution of the test cases to look in.
    @param modelDir: the location of the model run data
    @param benchDir: the location of the benchmark data
    '''
    def runStream(self, resolution, modelDir, benchDir):
        # Process the configure files
        print("  Stream " + resolution + " test in progress....")
        streamParser = Parser()
        self.modelConfigs['Stream ' + resolution], self.benchConfigs['Stream ' + resolution] = \
                streamParser.parseConfigurations(modelDir, benchDir, "*" + resolution + ".*.config")

        # Parse standard out
        self.fileTestDetails["Stream " + resolution] = streamParser.parseStdOutput(modelDir,"stream." + resolution + ".*.config.oe")

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = streamParser.getParserSummary()

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['Stream ' + resolution] = self.bit4bit('stream', modelDir, benchDir, resolution)
        for key, value in self.bitForBitDetails['Stream ' + resolution].iteritems():
            print ("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches += 1
            numberBitTests += 1

        self.summary['Stream ' + resolution] = [numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]
