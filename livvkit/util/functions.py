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
Module to hold LIVV specific functions 

@author: arbennett
"""
import os
import json
import errno
import shutil
import fnmatch
from datetime import datetime 

from util import variables
from util.datastructures import LIVVDict

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


def find_file(search_dir, file_pattern):
    """ Search for a file in a directory, and return the first match """
    for root, dirnames, fnames in os.walk(search_dir):
            for fname in fnames:
                if fnmatch.fnmatch(fname, file_pattern):
                    return os.path.join(root, fname)
    return "" 


def create_page_from_template(template_file, output_path):
    """ Copy the correct html template file to the output directory """
    shutil.copy(os.path.join(variables.website_dir, template_file), output_path)


def write_json(data, path, file_name):
    """
    Write out data to a json file.

    Args:
        data: A dictionary representation of the data to write out
        path: The directory to output the file in
        file_name: The name of the file to write out
    """
    if os.path.exists(path) and not os.path.isdir(path):
        return
    elif not os.path.exists(path):
        mkdir_p(path)
    with open(os.path.join(path, file_name),'w') as f:
        json.dump(data, f, indent=4)


def collect_cases(data_dir):
    """ Find all cases and subcases of a particular run type """
    cases = LIVVDict()
    for root, dirs, files in os.walk(data_dir):
        if not dirs:
            split_case = os.path.relpath(root,data_dir).split(os.sep)
            if split_case[0] not in cases: cases[split_case[0]] = []
            cases[split_case[0]].append("-".join(split_case[1:]))
    return cases


def setup_output():
    """ Copies old run data into a timestamped directory and sets up the new directory """
    # Check if we need to back up an old run
    if os.path.isdir(variables.index_dir):
        print("-------------------------------------------------------------------")
        print('Previous output data found in output directory!')
        try:
            f = open(variables.index_dir + os.sep + "data.txt", "r")
            prev_time = f.readline().replace(":","").replace("-","").replace(" ","_").rstrip()
            prev_comment = f.readline().rstrip()
            f.close()
        except IOError:
            prev_time = "bkd_"+datetime.now().strftime("%Y%m%d_%H%M%S")
            prev_comment = "Warning: could not find previous runtime and comment."

        print('   Backing up data to:')
        print('   ' + variables.index_dir + "_" + prev_time)
        print("-------------------------------------------------------------------")
        shutil.move(variables.index_dir, variables.index_dir + "_" + prev_time)
    else:
        print("-------------------------------------------------------------------")

    # Copy over js, css, & imgs directories from source
    mkdir_p(variables.website_dir)
    shutil.copytree(os.path.join(variables.website_dir,"css"), os.path.join(variables.index_dir,"css"))
    shutil.copytree(os.path.join(variables.website_dir,"js"), os.path.join(variables.index_dir,"js"))
    shutil.copytree(os.path.join(variables.website_dir,"imgs"), os.path.join(variables.index_dir,"imgs"))
    shutil.copy(os.path.join(variables.website_dir, "index.html"), 
                os.path.join(variables.index_dir, "index.html"))
    # Record when this data was recorded so we can make nice backups
    with open(variables.index_dir + os.sep + "data.txt", "w") as f:
        f.write(variables.timestamp + "\n")
        f.write(variables.comment)

