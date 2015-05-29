'''
Utility module to make setting up the index of the LIVV webpage easier.

Created Apr 21, 2015

@author arbennett
'''
import os
import shutil

import util.variables
import jinja2

'''
Prepare the index of the website.

@param testsRun: the top level names of each of the verification run
'''
def setup(testsRun):
    # Check if we need to back up an old run
    if os.path.exists(util.variables.indexDir):
        response = raw_input(os.linesep + "Found a duplicate of the output directory.  Would you like to create a backup before overwriting? (y/n)" + os.linesep)
        if response in ["yes", "Yes", "YES", "YEs", "y", "Y"]:
            if os.path.exists(util.variables.indexDir + "_backup"):
                shutil.rmtree(util.variables.indexDir + "_backup")
            shutil.copytree(util.variables.indexDir, util.variables.indexDir + "_backup")
        else:
            shutil.rmtree(util.variables.indexDir)

    # Create directory structure
    testDirs = [util.variables.indexDir, 
                util.variables.indexDir + os.sep + "validation", 
                util.variables.indexDir + os.sep + "verification", 
                util.variables.indexDir + os.sep + "performance"]
    for siteDir in testDirs:
        if not os.path.exists(siteDir):
            os.mkdir(siteDir);

    # Copy over css & imgs directories from source
    if os.path.exists(util.variables.indexDir + os.sep + "css"): shutil.rmtree(util.variables.indexDir + os.sep + "css")
    shutil.copytree(util.variables.websiteDir + os.sep + "css", util.variables.indexDir + os.sep + "css")
    if os.path.exists(util.variables.indexDir + os.sep + "imgs"): shutil.rmtree(util.variables.indexDir + os.sep + "imgs")
    shutil.copytree(util.variables.websiteDir + os.sep + "imgs", util.variables.indexDir + os.sep + "imgs")

    # Set up imgs directory to have sub-directories for each test
    for test in testsRun:
        if not os.path.exists(util.variables.imgDir + os.sep + test.capitalize() + os.sep + "bit4bit"):
            os.makedirs(util.variables.imgDir + os.sep + test.capitalize() + os.sep + "bit4bit")

'''
Build the index

@param verificationSummary: A summary of the verification verification run
@param performanceSummary: A summary of the performance verification run
@param validationSummary: A summary of the validation verification run
'''
def generate(verificationSummary, performanceSummary, validationSummary):
    # Where to look for page templates
    templateLoader = jinja2.FileSystemLoader(searchpath=util.variables.templateDir)
    templateEnv = jinja2.Environment(loader=templateLoader)

    # Create the index page
    templateFile = os.sep + "index.html"
    template = templateEnv.get_template(templateFile)

    templateVars = {"indexDir" : ".",
                    "verificationSummary" : verificationSummary,
                    "performanceSummary" : performanceSummary,
                    "validationSummary" : validationSummary,
                    "timestamp" : util.variables.timestamp,
                    "user" : util.variables.user,
                    "comment" : util.variables.comment,
                    "cssDir" : "css", 
                    "imgDir" : "imgs"}

    # Write out the index page
    outputText = template.render(templateVars)
    page = open(util.variables.indexDir + os.sep + "index.html", "w")
    page.write(outputText)
    page.close()
