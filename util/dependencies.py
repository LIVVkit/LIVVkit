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
Dependency management module for LIVV

Created on January 6, 2015

@author: arbennett
'''

#
# TODO : Try to import urllib2 before checking for setuptools.  If it's not available try using something
#        like curl or wget from a subprocess to download setuptools and then add urllib2 to the list of
#        dependencies to check (and obviously install)
#

import os
import sys
import urllib2
import subprocess

'''
Run all of the checks for dependencies required by LIVV

Checks if modules are used, and if they are checks to see
if they are loaded.  Then, checks for the necessary Python
libraries.  If any are missing they are installed via 
easy_install.  If easy_install isn't installed, that is 
also built.
'''
def check():
    cwd = os.getcwd()
    
    # The list of nonstandard python libraries that are used 
    libraryList = ["jinja2", "netCDF4", "numpy", "matplotlib"]
    binaryList = ["ncdiff", "ncl"]

    # Create a list to store all of the errors that were found
    depErrors = []

    print(os.linesep + "Beginning Dependency Checks........")

    # If we need to load modules for LCF machines do so now
    checkModules()

    # Make sure all environment variables are set
    if not os.environ.has_key("NCARG_ROOT"):
        depErrors.append("  NCARG_ROOT not found in environment")

    # Check to make sure that binary files are found
    print("    Checking for external programs....")
    for program in binaryList:
        found = False
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            filePath = os.path.join(path, program)
            if os.path.isfile(filePath) and os.access(filePath, os.X_OK):
                found = True
        if not found:
            depErrors.append("  " + program + " could not be found in system path.  Please install or update your path!")            
                


    # For the python dependencies we may need easy_install
    # Make sure we have it, and if not, build it       
    try:
        from setuptools.command import easy_install
    except ImportError:
        if not os.path.exists(cwd + os.sep + "deps"):
            os.mkdir(cwd + os.sep + "deps")
            sys.path.append(cwd + os.sep + "deps")
        installSetupTools()
        from setuptools.command import easy_install

    # Make sure all imports are going to work
    # And if they don't build a copy of the ones that are needed
    print("    Checking for external libraries....")
    libsInstalled=[]
    for lib in libraryList:
        try:
            __import__(lib)
            print("      Found " + lib + "!")
        except ImportError:
            print("      Could not find " + lib + ".  Building a copy for you...."),
            if not os.path.exists(cwd + os.sep + "deps"):
                os.mkdir(cwd + os.sep + "deps")
                sys.path.append(cwd + os.sep + "deps")
            easy_install.main(["--user",lib])
            libsInstalled.append(lib)

    if len(libsInstalled) > 0:
        print("------------------------------------------------------------------------------")
        print "  External Python Libraries have been installed!  Libraries installed:"
        for lib in libsInstalled:
            print("    " + lib)
        print("  Run LIVV again to continue.  ")
        print("------------------------------------------------------------------------------")
        exit(0)

    # Show all of the dependency errors that were found
    if len(depErrors) > 0:
        print("Uh oh!")
        print("")
        print("Errors checking dependencies.  Errors found: ")
        for err in depErrors: print(err)
        exit(len(depErrors))
    else:
        print("Okay!" + os.linesep + "Setting up environment....")

'''
Checks if the system running LIVV uses modules to load dependencies.

If the system does use modules, this method goes through and makes
sure that the correct modules are loaded.  Any modules that are needed
but haven't been loaded are added to a module loader script that the
user is prompted to source before running LIVV again.
'''
def checkModules():
    # Check to see if calling 'module list' is a real command
    cwd = os.getcwd()
    print("    Checking if modules need to be loaded"),
    modules = [
           "python/2.7.5", 
           "ncl/6.1.0", 
           "nco/4.3.9", 
           "python_matplotlib/1.3.1", 
           "hdf5/1.8.11", 
           "netcdf/4.1.3", 
           "python_numpy/1.8.0", 
           "python_netcdf4/1.0.6"
          ]
    checkCmd = ["bash", "-c", "module list"]
    checkCall = subprocess.Popen(checkCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = checkCall.communicate()

    # Find out if we need to check if modules are loaded
    if "bash: module: command not found" in err or \
            "bash: module: command not found" in out:
        print(" nope.  Continuing....")
        return
    else:
        # We need to check if all of the correct modules are loaded
        if not os.path.exists(cwd + os.sep + "deps"):
            os.mkdir(cwd + os.sep + "deps")
            sys.path.append(cwd + os.sep + "deps")
        f = open(cwd + os.sep + "deps" + os.sep + "modules", 'w')

        # Record the modules needed, the modules that have been loaded, and start a list for what's missing
        moduleListOutput = out.split() + err.split()
        modulesNeeded = []

        # Go through and find out if anything is missing
        for module in modules:
            f.write("module load " + module + "\n")
            if module not in moduleListOutput:
                modulesNeeded.append(module)
        f.close()

        # If anything was missing, tell the user what it was and how to fix it
        if len(modulesNeeded) != 0:
            print("")
            print("  ------------------------------------------")
            print("  | Could not find all necessary modules!  |")
            print("  ------------------------------------------")
            print("    Modules missing:")
            for each in modulesNeeded: print("   * " + each)
            print("")
            print("  ------------------------------------------")
            print("  | Use the command: source deps/modules   |")
            print("  | to load all of the missing modules.    |")
            print("  | then try running LIVV again.           |")
            print("  ------------------------------------------")
            exit(1)
        else:
            print(" found all required modules!")

'''
Installs setuptools under the user python libraries

If setuptools isn't found on a system it is probably the case that other
packages are also not available.   Once setuptools is installed we can
access the easy_install command from inside of LIVV if  any python
dependencies aren't satisfied
'''
def installSetupTools():
    # Specify where to download from
    cwd = os.getcwd()
    url = "https://bootstrap.pypa.io/ez_setup.py"
    fileName = "ez_setup.py"
    u = urllib2.urlopen(url)    
    f = open(cwd + os.sep + "deps" + os.sep + fileName, 'wb')

    block=8192
    while True:
        # We are downloading block by block - if we can't get anymore we must be done
        buffer = u.read(block)
        if not buffer: break
        f.write(buffer)
    os.system("python " + cwd + os.sep + "deps" + os.sep + fileName + " --user")
