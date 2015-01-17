'''
Generates the website through use of the templating library, jinja2.  Templates 
reduce the number of lines of code, as well as allows each type of page to only
be written once, and the data to be filled in automatically.

Created on Dec 8, 2014

@author: bzq
'''

import jinja2
import getpass
import time
import glob
import os

import livv

#
# Generates the html for the livv website
#
# input:
#   indexDir : the location to write the root of the webpages
#   testSummary : a basic summary of what tests were run
#
def generate(testSummary):
    # Set up directories
    cssDir = os.path.dirname(__file__) + "/livv_website/css"
    templateDir = os.path.dirname(__file__) + "/livv_website/templates"
    indexDir = livv.outputDir
    testDir = indexDir + "/tests"
    imgDir = indexDir + "/imgs"
        
    # Make sure they exist
    for siteDir in [cssDir, templateDir, indexDir, testDir, imgDir]:
        if not os.path.exists(siteDir):
            os.mkdir(siteDir);
        
    # Record some usage information
    testsRun = [test for sublist in testSummary[1] for test in sublist]
    timestamp = time.strftime("%m-%d-%Y %H:%M:%S")
    user = getpass.getuser()
    
    # Where to look for page templates
    templateLoader = jinja2.FileSystemLoader( searchpath=templateDir )
    templateEnv = jinja2.Environment( loader=templateLoader )
    
    # TODO: pull this section out of the index, and into the main livv piece
    # Set up the variables for the index page
    templateFile = "/index.html"
    template = templateEnv.get_template( templateFile )
         
    
    # Set up imgs directory to have sub-directories for each test
    for test in testNames:
        if not os.path.exists(imgDir + "/" + test):
            os.mkdir(imgDir + "/" + test)
    
    templateVars = {"indexDir" : indexDir,
                    "testsRun" : testsRun,
                    "timestamp" : timestamp,
                    "user" : user,
                    "testSummary" : testSummary,
                    "testCases" : testNames,
                    "cssDir" : cssDir }
    
    # Write out the index page
    outputText = template.render( templateVars )
    page = open(indexDir + "/index.html", "w")
    page.write(outputText)
    page.close()


#===================================================================================================
#  Below this will go into test specific class modules
#===================================================================================================
'''

    # Set up and write out each of the test pages
    templateFile = "/test.html"
    template = templateEnv.get_template( templateFile )

    # Process each of the testcases
    for i in range(len(testSummary[0])):
        # Map the test to the output html file and description
        test = testSummary[0][i]
        testDescription = testDescriptions[test]
        testsRun = testSummary[1][i]
        
        # Grab the images (note: returns the full path)
        testImgDir = imgDir + "/" + test
        testImages = glob.glob(testImgDir + "/*.png")
        testImages.append( glob.glob(testImgDir + "/*.jpg") )
        testImages.append( glob.glob(testImgDir + "/*.svg") )

        # Set up the template variables  
        templateVars = {"timestamp" : timestamp,
                        "user" : user,
                        "testName" : test,
                        "testDescription" : testDescription,
                        "testsRun" : testsRun,
                        "indexDir" : indexDir,
                        "cssDir" : cssDir, 
                        "imgDir" : testImgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/' + test + ".html", "w")
        page.write(outputText)
        page.close()
   '''      