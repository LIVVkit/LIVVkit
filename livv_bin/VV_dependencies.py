'''
Dependency management module for LIVV

Created on January 6, 2015

@author: bzq
'''

#
#
# TODO : Try to import urllib2 before checking for setuptools.  If it's not available try using something
#        like curl or wget from a subprocess to download setuptools and then add urllib2 to the list of
#        dependencies to check (and obviously install)
#
#

import os
import sys
import urllib2
import subprocess

import livv


## Run all of the checks for dependencies required by LIVV
#
def check():
    # Create a list to store all of the errors that were found
    depErrors = []
    
    print("")
    print("Beginning Dependency Checks........")
    
    # If we need to load modules for LCF machines do so now
    checkModules()
        
    # Make sure all environment variables are set
    if os.environ.get('NCARG_ROOT') == None:
        depErrors.append("  NCARG_ROOT not found in environment")
     
    # For the python dependencies we may need easy_install
    # Make sure we have it, and if not, build it       
    try:
        from setuptools.command import easy_install
    except ImportError:
        if not os.path.exists(livv.cwd + os.sep + "deps"):
            os.mkdir(livv.cwd + os.sep + "deps")
            sys.path.append(livv.cwd + os.sep + "deps")
        installSetupTools()
        from setuptools.command import easy_install

    # Make sure all imports are going to work
    # And if they don't build a copy of the ones that are needed
    print("    Checking for external libraries....")
    libraryList = ["jinja2", "netCDF4", "numpy", "matplotlib"]
    for lib in libraryList:
        try:
            __import__(lib)
            print("      Found " + lib + "!")
        except ImportError:
            print("      Could not find " + lib + ".  Building a copy for you...."),
            if not os.path.exists(livv.cwd + os.sep + "deps"):
                os.mkdir(livv.cwd + os.sep + "deps")
                sys.path.append(livv.cwd + os.sep + "deps")
            easy_install.main(["-U", "--install-dir " + livv.cwd + os.sep + "deps", lib])       
            print(" Done!")
        
    # Show all of the dependency errors that were found
    if len(depErrors) > 0:
        print("Uh oh!")
        print("")
        print("Errors checking dependencies.  Errors found: ")
        for err in depErrors: print(err)
        exit(len(depErrors))
    else:
        print("Okay!")
        print("Setting up environment....")


## Checks if the system running LIVV uses modules to load dependencies.  
#
#  If the system does use modules, this method goes through and makes 
#  sure that the correct modules are loaded.  Any modules that are needed
#  but haven't been loaded are added to a module loader script that the 
#  user is prompted to source before running LIVV again.     
#
def checkModules():
    # Check to see if calling 'module list' is a real command
    print("    Checking if modules need to be loaded"),
    checkCmd = ["bash", "-c", "module list"]
    checkCall = subprocess.Popen(checkCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = checkCall.communicate()
    
    # Find out if we need to check if modules are loaded
    if "bash: module: command not found" in err or \
            "bash: module: command not found" in out:
        # This system doesn't use modules for dependencies
        print(" nope.  Continuing....")
        return
    else:
        # We need to check if all of the correct modules are loaded
        if not os.path.exists(livv.cwd + os.sep + "deps"):
            os.mkdir(livv.cwd + os.sep + "deps")
            sys.path.append(livv.cwd + os.sep + "deps")
        f = open(livv.cwd + os.sep + "deps" + os.sep + "modules", 'w')

        # Record the modules needed, the modules that have been loaded, and start a list for what's missing
        modules = livv.modules
        moduleListOutput = out.split() + err.split()
        modulesNeeded = []
        
        # Go through and find out if anything is missing
        for module in livv.modules:
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


## Installs setuptools under the user python libraries
#
#  If setuptools isn't found on a system it is probably the case that other 
#  packages are also not available.   Once setuptools is installed we can 
#  access the easy_install command from inside of LIVV if  any python 
#  dependencies aren't satisfied
#
def installSetupTools():
    # Specify where to download from and figure out how big it's going to be
    url = "https://bootstrap.pypa.io/ez_setup.py"
    fileName = "ez_setup.py"
    u = urllib2.urlopen(url)
    f = open(livv.cwd + os.sep + "deps" + os.sep + fileName, 'wb')
    urlInfo = u.info()
    fileSize = int(urlInfo.getheaders("Content-Length")[0])
    
    # Download it
    sizeOnDisk = 0
    block=8192
    while True:
        # We are downloading block by block - if we can't get anymore we must be done
        buffer = u.read(block)
        if not buffer: break
        f.write(buffer)
    os.system("python " + livv.cwd + os.sep + "deps" + os.sep + fileName + " --user")
    
