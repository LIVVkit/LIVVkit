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

"""
Utility module to make setting up the index of the LIVV webpage easier.

Created Apr 21, 2015

@author arbennett
"""
import os
import errno
import shutil
from datetime import datetime

import util.variables
import jinja2

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


def setup():
    """
    Creates the directory structure that will have the web pages
    written to.
    
    Args:
        tests_run: the top level names of each of the tests run
    """
    # blindly make the output directory
    mkdir_p(util.variables.index_dir)

    # Check if we need to back up an old run
    if os.listdir(util.variables.index_dir):
        print("--------------------------------------------------------------------------")
        print('Previous output data found in output directory!')
        try:
            f = open(util.variables.index_dir + os.sep + "data.txt", "r")
            prev_time = f.readline().replace(":","").replace("-","").replace(" ","_").rstrip()
            prev_comment = f.readline().rstrip()
            f.close()
        except IOError:
            prev_time = "bkd_"+datetime.now().strftime("%Y%m%d_%H%M%S")
            prev_comment = "Warning: could not find previous runtime and comment."

        print('   Backing up data to:')
        print('   ' + util.variables.index_dir + "_" + prev_time)
        print("--------------------------------------------------------------------------")
        shutil.move(util.variables.index_dir, util.variables.index_dir + "_" + prev_time)
        mkdir_p(util.variables.index_dir)
    else:
        print("--------------------------------------------------------------------------")
 

    # Copy over css & imgs directories from source
    shutil.copytree(util.variables.website_dir + os.sep + "css", util.variables.index_dir + os.sep + "css")
    shutil.copytree(util.variables.website_dir + os.sep + "imgs", util.variables.index_dir + os.sep + "imgs")

    # Record when this data was recorded so we can make nice backups
    f = open(util.variables.index_dir + os.sep + "data.txt", "w")
    f.write(util.variables.timestamp + "\n")
    f.write(util.variables.comment)
    f.close()


def generate(numerics_summary, verification_summary, performance_summary, validation_summary):
    """
    Build the index
    
    Args:
        verification_summary: A summary of the verification verification run
        performance_summary: A summary of the performance verification run
        validation_summary: A summary of the validation verification run
    """
    template_loader = jinja2.FileSystemLoader(searchpath=util.variables.template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = os.sep + "index.html"
    template = template_env.get_template(template_file)
    template_vars = {"index_dir" : ".",
                    "numerics_summary" : numerics_summary,
                    "verification_summary" : verification_summary,
                    "performance_summary" : performance_summary,
                    "validation_summary" : validation_summary,
                    "timestamp" : util.variables.timestamp,
                    "user" : util.variables.user,
                    "comment" : util.variables.comment,
                    "css_dir" : "css", 
                    "img_dir" : "imgs"}
    output_text = template.render(template_vars)
    page = open(util.variables.index_dir + os.sep + "index.html", "w")
    page.write(output_text)
    page.close()
