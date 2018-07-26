# coding=utf-8
# Copyright (c) 2015-2018, UT-BATTELLE, LLC
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
Storage for global variables.  These are set upon startup in the options module
"""
import os
import time
import getpass
import platform
import socket

from livvkit import bundles
from livvkit import resources

__version_info__ = (2, 1, 6)
__version__ = '.'.join(str(vi) for vi in __version_info__)

cwd = os.getcwd()
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
user = getpass.getuser()
machine = socket.gethostname()
os_type = platform.system() + " " + platform.release()

comment = ""

resource_dir = os.path.dirname(resources.__file__)
bundle_dir = os.path.dirname(bundles.__file__)

# directory vars -- filled in by options
output_dir = None
index_dir = None
model_dir = None
bench_dir = None

# direct access to some optional imports
model_bundle = None

numerics_model_config = None
numerics_model_module = None

verification_model_config = None
verification_model_module = None

performance_model_config = None
performance_model_module = None

validation_model_configs = None

# optional flags
verify = False
validate = False
publish = False
