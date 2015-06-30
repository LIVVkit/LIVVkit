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
Dependency management module for LIVV

Created on January 6, 2015

@author: arbennett
"""

#
# TODO : Try to import urllib2 before checking for setuptools.  If it's not available try using something
#        like curl or wget from a subprocess to download setuptools and then add urllib2 to the list of
#        dependencies to check (and obviously install)
#

import os
import sys
import urllib2
import subprocess


def check():
    """
    Run all of the checks for dependencies required by LIVV
    
    Checks if modules are used, and if they are checks to see
    if they are loaded.  Then, checks for the necessary Python
    libraries.  If any are missing they are installed via 
    easy_install.  If easy_install isn't installed, that is 
    also built.
    """
    cwd = os.getcwd()
    
    # The list of nonstandard python libraries that are used 
    library_list = ["jinja2", "netCDF4", "numpy", "matplotlib"]
    # The list of command line programs needed
    binary_list = ["ncdiff", "ncl"]
    error_list = []
    print(os.linesep + "Beginning Dependency Checks........")

    # If we need to load modules for LCF machines do so now
    # check_modules()

    # Make sure all environment variables are set
    if not os.environ.has_key("NCARG_ROOT"):
        error_list.append("  NCARG_ROOT not found in environment")

    # Check to make sure that binary files are found
    print("    Checking for external programs....")
    for program in binary_list:
        found = False
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            file_path = os.path.join(path, program)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                found = True
        if not found:
            error_list.append("  " + program + " could not be found in system path.  Please install or update your path!")            
                
    # For the python dependencies we may need easy_install
    # Make sure we have it, and if not, build it       
    try:
        from setuptools.command import easy_install
    except ImportError:
        if not os.path.exists(cwd + os.sep + "deps"):
            os.mkdir(cwd + os.sep + "deps")
            sys.path.append(cwd + os.sep + "deps")
        install_setup_tools()
        from setuptools.command import easy_install

    # Make sure all imports are going to work
    # And if they don't build a copy of the ones that are needed
    print("    Checking for external libraries....")
    libs_installed=[]
    for lib in library_list:
        try:
            __import__(lib)
            print("      Found " + lib + "!")
        except ImportError:
            print("      Could not find " + lib + ".  Building a copy for you...."),
            if not os.path.exists(cwd + os.sep + "deps"):
                os.mkdir(cwd + os.sep + "deps")
                sys.path.append(cwd + os.sep + "deps")
            easy_install.main(["--user",lib])
            libs_installed.append(lib)

    if len(libs_installed) > 0:
        print("")
        print("")        
        print("------------------------------------------------------------------------------")
        print "  External Python Libraries have been installed!  Libraries installed:"
        for lib in libs_installed:
            print("    " + lib)
        print("  Run LIVV again to continue.  ")
        print("------------------------------------------------------------------------------")
        print("")
        exit(0)

    # Show all of the dependency errors that were found
    if len(error_list) > 0:
        print("Uh oh!")
        print("")
        print("------------------------------------------------------------------------------")
        print("Errors checking dependencies.  Errors found: ")
        for err in error_list: print(err)
        print("------------------------------------------------------------------------------")
        print("")
        exit(len(error_list))
    else:
        print("Okay!" + os.linesep + "Setting up environment....")


def check_modules():
    """
    Checks if the system running LIVV uses modules to load dependencies.
    
    If the system does use modules, this method goes through and makes
    sure that the correct modules are loaded.  Any modules that are needed
    but haven't been loaded are added to a module loader script that the
    user is prompted to source before running LIVV again.
    """
    # Check to see if calling 'module list' is a real command
    cwd = os.getcwd()
    print("    Checking if modules need to be loaded"),
    modules = [
           "python", 
           "ncl", 
           "nco", 
           "python_matplotlib", 
           "hdf5", 
           "netcdf", 
           "python_numpy", 
           "python_netcdf4"
          ]
    check_cmd = ["bash", "-c", "module list"]
    check_call = subprocess.Popen(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = check_call.communicate()

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
        module_list_output = out.split() + err.split()
        modules_needed = []

        # Go through and find out if anything is missing
        for module in modules:
            f.write("module load " + module + "\n")
            if module+'*' not in module_list_output:
                modules_needed.append(module)
        f.close()

        # If anything was missing, tell the user what it was and how to fix it
        if len(modules_needed) != 0:
            print("")
            print("  ------------------------------------------")
            print("  | Could not find all necessary modules!  |")
            print("  ------------------------------------------")
            print("    Modules missing:")
            for each in modules_needed: print("   * " + each)
            print("")
            print("  ------------------------------------------")
            print("  | Use the command: source deps/modules   |")
            print("  | to load all of the missing modules.    |")
            print("  | then try running LIVV again.           |")
            print("  ------------------------------------------")
            exit(1)
        else:
            print(" found all required modules!")


def install_setup_tools():
    """
    Installs setuptools under the user python libraries
    
    If setuptools isn't found on a system it is probably the case that other
    packages are also not available.   Once setuptools is installed we can
    access the easy_install command from inside of LIVV if  any python
    dependencies aren't satisfied
    """
    cwd = os.getcwd()
    url = "https://bootstrap.pypa.io/ez_setup.py"
    file_name = "ez_setup.py"
    u = urllib2.urlopen(url)    
    f = open(cwd + os.sep + "deps" + os.sep + file_name, 'wb')

    block=8192
    while True:
        # We are downloading block by block - if we can't get anymore we must be done
        buff = u.read(block)
        if not buff: break
        f.write(buff)
    os.system("python " + cwd + os.sep + "deps" + os.sep + file_name + " --user")
