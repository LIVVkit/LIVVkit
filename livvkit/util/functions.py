# Copyright (c) 2015,2016, UT-BATTELLE, LLC
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
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import json
import errno
import shutil
import fnmatch
from datetime import datetime

import livvkit


def mkdir_p(path):
    """
    Make parent directories as needed and no error if existing. Works like `mkdir -p`.
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def merge_dicts(dict1, dict2):
    """ Merge two dictionaries and return the result """
    tmp = dict1.copy()
    tmp.update(dict2)
    return tmp


def get_leaves(d):
    """ Get the leaves of a nested dictionary """
    leaves = []
    for key, val in d.items():
        if issubclass(type(val), dict):
            leaves.append(get_leaves(val))
        else:
            return val
    return leaves


def parse_gptl(file_path, var_list):
    """
    Read a GPTL timing file and extract some data.

    Args:
        file_path: the path to the GPTL timing file
        var_list: a list of strings to look for in the file

    Returns:
        A dict containing key-value pairs of the livvkit
        and the times associated with them
    """
    timing_result = dict()
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            for var in var_list:
                for line in f:
                    if var in line:
                        timing_result[var] = float(line.split()[4])/int(line.split()[2])
                        break
    return timing_result


def find_file(search_dir, file_pattern):
    """
    Search for a file in a directory, and return the first match.
    If the file is not found return an empty string

    Args:
        search_dir: The root directory to search in
        file_pattern: A unix-style wildcard pattern representing
            the file to find

    Returns:
        The path to the file if it was found, otherwise an empty string
    """
    for root, dirnames, fnames in os.walk(search_dir):
            for fname in fnames:
                if fnmatch.fnmatch(fname, file_pattern):
                    return os.path.join(root, fname)
    return ""


def sort_processor_counts(p_string):
    """ Simple wrapper to help sort processor counts """
    return int(p_string.split('-')[0][1:])


def sort_scale(s_string):
    """ Simple wrapper to help sort scale sizes """
    return int(s_string[1:])


def create_page_from_template(template_file, output_path):
    """ Copy the correct html template file to the output directory """
    mkdir_p(os.path.dirname(output_path))
    shutil.copy(os.path.join(livvkit.resource_dir, template_file), output_path)


def read_json(file_path):
    """ Read in a json file and return a dictionary representation """
    config = {}
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
    except:
        pass
    return config


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
    with open(os.path.join(path, file_name), 'w') as f:
        json.dump(data, f, indent=4)


def collect_cases(data_dir):
    """ Find all cases and subcases of a particular run type """
    cases = {}
    for root, dirs, files in os.walk(data_dir):
        if not dirs:
            split_case = os.path.relpath(root, data_dir).split(os.sep)
            if split_case[0] not in cases:
                cases[split_case[0]] = []
            cases[split_case[0]].append("-".join(split_case[1:]))
    return cases


def setup_output():
    """
    Set up the directory structure for the output.  Copies old run
    data into a timestamped directory and sets up the new directory
    """
    # Check if we need to back up an old run
    if os.path.isdir(livvkit.index_dir):
        print("-------------------------------------------------------------------")
        print('Previous output data found in output directory!')
        try:
            f = open(livvkit.index_dir + os.sep + "data.txt", "r")
            prev_time = f.readline().replace(":", "").replace("-", "").replace(" ", "_").rstrip()
            f.close()
        except IOError:
            prev_time = "bkd_"+datetime.now().strftime("%Y%m%d_%H%M%S")
        print('   Backing up data to:')
        print('   ' + livvkit.index_dir + "_" + prev_time)
        print("-------------------------------------------------------------------")
        shutil.move(livvkit.index_dir, livvkit.index_dir + "_" + prev_time)
    else:
        print("-------------------------------------------------------------------")

    # Copy over js, css, & imgs directories from source
    shutil.copytree(os.path.join(livvkit.resource_dir, "css"),
                    os.path.join(livvkit.index_dir, "css"))
    shutil.copytree(os.path.join(livvkit.resource_dir, "js"),
                    os.path.join(livvkit.index_dir, "js"))
    shutil.copytree(os.path.join(livvkit.resource_dir, "imgs"),
                    os.path.join(livvkit.index_dir, "imgs"))
    shutil.copy(os.path.join(livvkit.resource_dir, "index.html"),
                os.path.join(livvkit.index_dir, "index.html"))
    # Record when this data was recorded so we can make nice backups
    with open(livvkit.index_dir + os.sep + "data.txt", "w") as f:
        f.write(livvkit.timestamp + "\n")
        f.write(livvkit.comment)


def Optional(func):
    def func_wrapper():
        return
    return func_wrapper
