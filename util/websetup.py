'''
Utility module to make setting up the index of the LIVV webpage easier.

Created Apr 21, 2015

@author arbennett
'''
import os
import shutil

import livv
import jinja2

## Prepare the index of the website.
#
#  input:
#    @param testsRun: the top level names of each of the verification run
#
def setup(testsRun):
    # Check if we need to back up an old run
    if os.path.exists(livv.indexDir):
        response = raw_input("Found a duplicate of the output directory.  Would you like to create a backup before overwriting? (y/n)")
        if response in ["yes", "Yes", "YES", "YEs", "y", "Y"]:
            if os.path.exists(livv.indexDir + "_backup"):
                shutil.rmtree(livv.indexDir + "_backup")
            shutil.copytree(livv.indexDir, livv.indexDir + "_backup")
        else:
            shutil.rmtree(livv.indexDir)

    # Create directory structure
    testDirs = [livv.indexDir, 
                livv.indexDir + os.sep + "validation", 
                livv.indexDir + os.sep + "verification", 
                livv.indexDir + os.sep + "performance"]
    for siteDir in testDirs:
        if not os.path.exists(siteDir):
            os.mkdir(siteDir);

    # Copy over css && imgs directories from source
    if os.path.exists(livv.indexDir + os.sep + "css"): shutil.rmtree(livv.indexDir + os.sep + "css")
    shutil.copytree(livv.websiteDir + os.sep + "css", livv.indexDir + os.sep + "css")
    if os.path.exists(livv.indexDir + os.sep + "imgs"): shutil.rmtree(livv.indexDir + os.sep + "imgs")
    shutil.copytree(livv.websiteDir + os.sep + "imgs", livv.indexDir + os.sep + "imgs")

    # Set up imgs directory to have sub-directories for each test
    for test in testsRun:
        if not os.path.exists(livv.indexDir + os.sep + "imgs" + os.sep + test + os.sep + "bit4bit"):
            os.makedirs(livv.imgDir + os.sep + test + os.sep + "bit4bit")


## Build the index
#
#  input:
#    @param verificationSummary: A summary of the verification verification run
#    @param performanceSummary: A summary of the performance verification run
#    @param validationSummary: A summary of the validation verification run
#
def generate(verificationSummary, performanceSummary, validationSummary):
    # Where to look for page templates
    templateLoader = jinja2.FileSystemLoader(searchpath=livv.templateDir)
    templateEnv = jinja2.Environment(loader=templateLoader)

    # Create the index page
    templateFile = os.sep + "index.html"
    template = templateEnv.get_template(templateFile)

    templateVars = {"indexDir" : ".",
                    "verificationSummary" : verificationSummary,
                    "performanceSummary" : performanceSummary,
                    "validationSummary" : validationSummary,
                    "timestamp" : livv.timestamp,
                    "user" : livv.user,
                    "comment" : livv.comment,
                    "cssDir" : "css", 
                    "imgDir" : "imgs"}

    # Write out the index page
    outputText = template.render(templateVars)
    page = open(livv.indexDir + os.sep + "index.html", "w")
    page.write(outputText)
    page.close()
