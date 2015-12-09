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

import os
import glob
import numpy as np
import subprocess
import jinja2
from netCDF4 import Dataset

import util.variables

class AbstractTest(object):
    """ Defines some basic operations that validation tests might use"""

    def __init__(self):
        """ Constructor """
        self.name = 'Default'
        self.description = 'About this test'
        self.summary = [0,0,0,0,0]
        
        return

    
    def generate(self):
        """ Build the output page """
        template_loader = jinja2.FileSystemLoader(searchpath=util.variables.template_dir)
        template_env = jinja2.Environment(loader=template_loader, extensions=["jinja2.ext.do",])
        template_file = "/validation_test.html"
        template = template_env.get_template(template_file)
        index_dir = "../.."
        css_dir = index_dir + "/css"
        img_dir = index_dir + "/imgs"
        test_imgDir = util.variables.index_dir + os.sep + "validation" + os.sep + \
                      self.name + os.sep + "imgs"
        test_images = [os.path.basename(img) for img in glob.glob(test_imgDir + os.sep + "*.png")]
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + "*.jpg")])
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + "*.svg")])
        test_images = filter(None, test_images)
        template_vars = {"timestamp" : util.variables.timestamp,
                        "user" : util.variables.user,
                        "comment" : util.variables.comment,
                        "test_name" : self.name.capitalize(),
                        "index_dir" : index_dir,
                        "css_dir" : css_dir,
                        "img_dir" : img_dir,
                        "test_imgDir" : os.path.relpath(test_imgDir, test_imgDir+os.sep+'../'),
                        "test_name" : self.name.capitalize(),
                        "test_description" : self.description,
                        "test_images" : test_images}
        output_text = template.render( template_vars )
        page = open(util.variables.index_dir + os.sep + "validation" + os.sep + self.name + os.sep + self.name + '.html', "w")
        page.write(output_text)
        page.close()
