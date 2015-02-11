'''
Master module for shelf test cases

Created on Dec 8, 2014

@author: bzq
'''

import livv
from livv import *
from livv_bin.VV_test import *
import jinja2

# # Main class for handling shelf test cases.
#
#  The shelf test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles the confined and circular variations of the shelf cases.
#
class Shelf(AbstractTest):
    
    # # Constructor
    #
    def __init__(self):
        # Mapping of result codes to results
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        
        # Keep track of what shelf test have been run
        self.shelfTestsRun = []
        self.shelfBitForBitDetails = dict()
        self.shelfTestFiles = []
        self.shelfTestDetails = []
        self.shelfFileTestDetails = []
    
        self.name = "shelf"
        self.description = "A blank description"
    
    # # Return the name of the test
    #
    #  output:
    #    @returns name : shelf
    #
    def getName(self):
        return self.name
    
    
    # # Runs the shelf specific test case.  
    #
    #  When running a test this call will record the specific test case 
    #  being run.  Each specific test case string is mapped to the 
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param testCase : the string indicator of the test to run
    #
    def run(self, test):
        # Common run 
        self.shelfTestsRun.append(test)
        
        # Map the case names to the case functions
        callDict = {'confined-shelf' : self.runConfined,
                    'circular-shelf' : self.runCircular}
        
        # Call the correct function
        if callDict.has_key(test):
            callDict[test]()
        else: 
            print("  Could not find test code for shelf test: " + test)
         
        # More common postprocessing
        return
        
    
    # # Creates the output test page
    #
    #  The generate method will create a shelf.html page in the output directory.
    #  This page will contain a detailed list of the results from LIVV.  
    #
    def generate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath=livv.templateDir)
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateFile = "/test.html"
        template = templateEnv.get_template(templateFile)
        
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs/shelf"
        
        testImgDir = livv.imgDir + os.sep + "shelf"
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.svg")])

        self.shelfFileTestDetails = zip(self.shelfTestFiles, self.shelfTestDetails)

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "testName" : self.getName(),
                        "indexDir" : indexDir,
                        "cssDir" : cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.shelfTestsRun,
                        "bitForBitDetails" : self.shelfBitForBitDetails,
                        "testHeader" : livv.parserVars,
                        "testDetails" : self.shelfFileTestDetails,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render(templateVars)
        page = open(testDir + '/shelf.html', "w")
        page.write(outputText)
        page.close()  
    
    
    # # Perform V&V on the confined shelf case
    # 
    def runConfined(self):
        print("  Confined Shelf test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/confined-shelf' + livv.dataDir)
        test = re.compile("confined-shelf.*out.*")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.shelfTestDetails.append(self.parse(livv.inputDir + '/confined-shelf' + livv.dataDir + "/" + file))
            self.shelfTestFiles.append(file)
        
        # Create the plots
        self.plotConfined()

        # Run bit for bit test
        self.shelfBitForBitDetails['confined-shelf'] = self.bit4bit('/confined-shelf')
        for key, value in self.shelfBitForBitDetails['confined-shelf'].iteritems():
            print ("    {:<30} {:<10}".format(key, value))

        return 0  # zero returns success
    
    # # Plot some details for the confined shelf case
    # 
    def plotConfined(self):
        print("    This is a placeholder method.")
    
    # # Perform V&V on the circular shelf case
    # 
    def runCircular(self):
        print("  Circular Shelf test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/circular-shelf' + livv.dataDir)
        test = re.compile("confined-shelf.*out.*")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.shelfTestDetails.append(self.parse(livv.inputDir + '/circular-shelf' + livv.dataDir + "/" + file))
            self.shelfTestFiles.append(file)
        
        # Create the plots
        self.plotConfined()

        # Run bit for bit test
        self.shelfBitForBitDetails['circular-shelf'] = self.bit4bit('/circular-shelf')
        for key, value in self.shelfBitForBitDetails['circular-shelf'].iteritems():
            print ("    {:<30} {:<10}".format(key, value))

        return 0  # zero returns success
    
    # # Plot some details from the confined shelf case
    # 
    def plotCircular(self):
        print("    This is a placeholder method.")
