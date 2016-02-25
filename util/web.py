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
    # Check if we need to back up an old run
    if os.path.isdir(util.variables.index_dir):
        print("-------------------------------------------------------------------")
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
        print("-------------------------------------------------------------------")
        shutil.move(util.variables.index_dir, util.variables.index_dir + "_" + prev_time)
    else:
        print("-------------------------------------------------------------------")

    # Copy over css & imgs directories from source
    shutil.copytree(util.variables.website_dir, util.variables.index_dir)

    # Record when this data was recorded so we can make nice backups
    with open(util.variables.index_dir + os.sep + "data.txt", "w") as f:
        f.write(util.variables.timestamp + "\n")
        f.write(util.variables.comment)

