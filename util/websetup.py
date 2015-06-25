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


'''
Utility module to make setting up the index of the LIVV webpage easier.

Created Apr 21, 2015

@author arbennett
'''
import os
import errno
import shutil
from datetime import datetime

import util.variables
import jinja2

'''
Prepare the index of the website.

@param testsRun: the top level names of each of the verification run
'''

def mkdir_p(path):
    """
    Make parent directories as needed and no error if existing. Works like `mkdir -p`.
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def setup(testsRun):
    # blindly make the output directory
    mkdir_p(util.variables.indexDir)

    # Check if we need to back up an old run
    if os.listdir(util.variables.indexDir):
        response = raw_input(os.linesep + "Found a duplicate of the output directory.  Would you like to create a backup before overwriting? (y/n)" + os.linesep)
        if response in ["yes", "Yes", "YES", "YEs", "y", "Y"]:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.move(util.variables.indexDir, util.variables.indexDir + "_bkd_" + stamp)
        else:
            shutil.rmtree(util.variables.indexDir)

    # Create directory structure
    testDirs = [util.variables.indexDir + os.sep + "validation", 
                util.variables.indexDir + os.sep + "verification", 
                util.variables.indexDir + os.sep + "performance"]
    for siteDir in testDirs:
        mkdir_p(siteDir);

    # Copy over css & imgs directories from source
    shutil.copytree(util.variables.websiteDir + os.sep + "css", util.variables.indexDir + os.sep + "css")
    shutil.copytree(util.variables.websiteDir + os.sep + "imgs", util.variables.indexDir + os.sep + "imgs")

    # Set up imgs directory to have sub-directories for each test
    for test in testsRun:
        mkdir_p(util.variables.imgDir + os.sep + test.getName().capitalize() + os.sep + "bit4bit")

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
