'''
Master script for dome test cases

Created on Dec 8, 2014

@author: bzq
'''

import re
import os
import sys
import glob
import subprocess

import livv
from livv import *
import livv_bin.VV_checks as check
import livv_bin.VV_utilities as util
import livv_bin.VV_outprocess as process
from livv_bin.VV_test import *

class Ismip(AbstractTest):
    
    #
    # Constructor
    #
    def __init__(self):
        self.ismipTestsRun = []
        self.ismipBitForBitDetails = dict()
        self.ismipTestFiles = []
        self.ismipTestDetails = []
        self.ismipFileTestDetails = []
        
        self.name = "ismip"
        self.description = "Simulates steady ice flow over a surface with periodic boundary conditions"
    
    #
    # Return the name of the test
    #
    def getName(self):
        return self.name
    
    
    #
    # Runs the dome specific test case.  Calls some shared resources and
    # some diagnostic/evolving case specific methods.
    #
    #
    #
    def run(self, testCase):
        # Common run 
        self.ismipTestsRun.append(testCase)
        
        # Map the case names to the case functions
        callDict = {'ismip-hom-a/20km' : self.runLargeA,
                    'ismip-hom-c/20km' : self.runLargeC,
                    'ismip-hom-a/80km' : self.runSmallA,
                    'ismip-hom-c/80km' : self.runSmallC }
        
        # Call the correct function
        callDict[testCase]()
         
        # More common postprocessing
        return
    
    
    #
    #  Description
    #
    #
    def generate(self):
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        templateFile = "/test.html"
        template = templateEnv.get_template( templateFile )
        
        testImgDir = imgDir + os.sep + "ismip"
        testImages = glob.glob(testImgDir + os.sep + "*.png")
        testImages.append( glob.glob(testImgDir + "/*.jpg") )
        testImages.append( glob.glob(testImgDir + "/*.svg") )

        self.ismipFileTestDetails = zip(self.ismipTestFiles, self.ismipTestDetails)

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testName" : self.getName(),
                        "indexDir" : livv.indexDir,
                        "cssDir" : livv.cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.ismipTestsRun,
                        "bitForBitDetails" : self.ismipBitForBitDetails,
                        "testDetails" : self.ismipFileTestDetails,
                        "imgDir" : testImgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/ismip.html', "w")
        page.write(outputText)
        page.close()        
    
    
    #
    # Runs the diagnostic dome specific test case code.  
    #
    #
    #    
    def runLargeA(self):
        print("  Ismip-hom-A 20km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + livv.dataDir + '/ismip-hom-a/20km')
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + livv.dataDir + '/ismip-hom-a/20km/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('a','20')

        # Run bit for bit test
        self.ismipBitForBitDetails = self.bit4bit('/ismip-hom-a/20km')
        for key, value in self.ismipBitForBitDetails.iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runLargeC(self):
        print("  Ismip-hom-C 20km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + livv.dataDir + '/ismip-hom-c/20km')
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + livv.dataDir + '/ismip-hom-c/20km/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('c','20')

        # Run bit for bit test
        self.ismipBitForBitDetails = self.bit4bit('/ismip-hom-c/20km')
        for key, value in self.ismipBitForBitDetails.iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runSmallA(self):
        print("  Ismip-hom-A 80km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + livv.dataDir + '/ismip-hom-a/80km')
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + livv.dataDir + '/ismip-hom-a/80km/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('a','80')

        # Run bit for bit test
        self.ismipBitForBitDetails = self.bit4bit('/ismip-hom-a/80km')
        for key, value in self.ismipBitForBitDetails.iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runSmallC(self):
        print("  Ismip-hom-C 80km test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + livv.dataDir + '/ismip-hom-c/80km')
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.ismipTestDetails.append(self.parse(livv.inputDir + livv.dataDir + '/ismip-hom-c/80km/' + file))
            self.ismipTestFiles.append(file)
        
        # Create the plots
        self.plot('c','80')

        # Run bit for bit test
        self.ismipBitForBitDetails = self.bit4bit('/ismip-hom-c/80km')
        for key, value in self.ismipBitForBitDetails.iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success

    #
    # Create the plots
    #
    #
    def plot(self, aOrC, size):
        print "    Generating ismip-hom-" + aOrC + "-" + size + "km plot...." 
        print "    This is just a dummy method.  Updates coming soon!"