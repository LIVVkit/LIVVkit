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

#
# Generates the html for the livv website
#
# input:
#   indexDir : the location to write the root of the webpages
#   testSummary : a basic summary of what tests were run
#
def generate(indexDir, testSummary):
    # Set up directories
    cssDir = os.path.dirname(__file__) + "/css"
    templateDir = os.path.dirname(__file__) + "/templates"
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
    testDict = { "dome30/diagnostic" : "dome",
                "dome30/evolving" : "dome",
                "ismip-hom-a/80km" : "ismip",
                "ismip-hom-c/80km" : "ismip",
                "ismip-hom-a/20km" : "ismip",
                "ismip-hom-c/20km" : "ismip",
                "RUN_GIS_4KM" : "gis",
                "RUN_GIS_2KM" : "gis",
                "RUN_GIS_1KM" : "gis",
                "circular-shelf" : "shelf",
                "confined-shelf" : "shelf"}
    
    testNames = [ "dome", "gis", "ismip", "validation", "shelf" ]
    testDescriptions = {"dome" : "3-D paraboloid dome of ice with a circular, 60 km" +
                            " diameter base sitting on a flat bed. The horizontal" +
                            " spatial resolution studies are 2 km, 1 km, 0.5 km" + 
                            " and 0.25 km, and there are 10 vertical levels. For this" +
                            " set of experiments a quasi no-slip basal condition in" +
                            " imposed by setting. A zero-flux boundary condition is" +
                            " applied to the dome margins. ",
                        "gis" : "Attributes: This test case represents the Greenland ice" +
                            " sheet (GIS) at different spatial resolutions (10km and 5km)." +
                            " A quasi-no slip boundary condition is applied at the bed. As" +
                            " with the dome test cases, a zero-flux boundary condition is" +
                            " applied to the lateral margins. In all test cases, the ice" +
                            " is taken as isothermal with a constant and uniform rate factor of.",
                        "ismip" : "Simulates steady ice flow over a surface with periodic boundary conditions",
                        "validation" : "A description of the validation tests.",
                        "shelf" : "A description of the shelf tests."
                        }                    
    
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
        