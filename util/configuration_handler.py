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
Contains the specifications for how to handle preconfigured options

Created on Dec 23, 2014

@authors: arbennett, jhkennedy
"""

import os
import util.variables

def save(options):
    """
    Write a configuration file to user specified file.
    
    Args:
        options: an argparse Namespace 
    """
         
    # get options to save
    save_options = []
    for opt, value in vars(options).items():
        # ignore these options
        if opt in ['load','save']:
            pass
        # boolean options
        elif opt in ['performance']:
            save_options.append("--"+opt.replace('_','-')+"\n")
        # all other options
        else:
            save_options.append("--"+opt.replace('_','-')+"="+str(value)+"\n")


    # get configuration file name
    save_path, save_name = os.path.split(options.save)
    if not save_path:
        save_path = util.variables.cwd + os.sep + 'configurations'
    save_file = os.path.join(save_path, save_name)

    # write configuration file
    with open(save_file, 'w') as sf:
        for opt in save_options:
            sf.write(opt)
