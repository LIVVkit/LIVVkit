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
Storage for global variables.  These are set upon startup in the main 
livv.py module

Created on May 5th, 2015

@authors: arbennett, jhkennedy
"""
cwd            = ''
config_dir      = ''
input_dir       = ''
benchmark_dir   = ''
output_dir      = ''
img_dir         = ''
comment        = ''
timestamp      = ''
user           = ''
website_dir     = ''
template_dir    = ''
index_dir       = ''
verification   = ''
verifications  = []
performance    = ''
performances  = []
validation     = ''
validations   = []

# Modules that need to be loaded on big machines
modules = []

# A list of the information that should be looked for in the stdout of model output
parser_vars = []

# Variables to measure when parsing through timing summaries
timing_vars = []

# Dycores to try to parse output for
dycores = []

def print_vars():
    """ Print out the variables that are contained in this module """
    for k,v in globals().iteritems():
        if not str(k).startswith('__'):
            print str(k) + " = " + str(v)
