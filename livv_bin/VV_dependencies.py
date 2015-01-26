'''
Dependency management for LIVV

Created on January 6, 2015

@author: bzq
'''

import os
import sys
import hashlib
import shutil
import urllib2
import tarfile
import subprocess

import livv
from livv import *

#
# Run all of the checks for dependencies required by LIVV
#
#
def check():
    # Create a list to store all of the errors that were found
    depErrors = []
    
    print("")
    print("Beginning Dependency Checks........")
    
    # Make sure all environment variables are set
    if os.environ.get('NCARG_ROOT') == None:
        depErrors.append("  NCARG_ROOT not found in environment")
        
    # If we need to load modules for LCF machines do so now
    loadModules()
    
    try:
        from setuptools.command import easy_install
    except ImportError:
        if not os.path_exists(livv.cwd + os.sep + "deps"):
            os.mkdir(livv.cwd + os.sep + "deps")
            sys.path.append(livv.cwd + os.sep + "deps")
        installSetupTools()
        from setuptools.command import easy_install

    # Make sure all imports are going to work
    try:
        __import__("jinja2")
    except ImportError:
        if not os.path_exists(livv.cwd + os.sep + "deps"):
            os.mkdir(livv.cwd + os.sep + "deps")
            sys.path.append(livv.cwd + os.sep + "deps")
        easy_install.main(["-U", "--install-dir " + livv.cwd + os.sep + "deps", "jinja2"])       
    try:
        __import__("netCDF4")
    except ImportError:
        if not os.path_exists(livv.cwd + os.sep + "deps"):
            os.mkdir(livv.cwd + os.sep + "deps")
            sys.path.append(livv.cwd + os.sep + "deps")
        easy_install.main(["-U", "--install-dir " + livv.cwd + os.sep + "deps", "netCDF4"])
    try:
        __import__("numpy")
    except ImportError:
        if not os.path_exists(livv.cwd + os.sep + "deps"):
            os.mkdir(livv.cwd + os.sep + "deps")
            sys.path.append(livv.cwd + os.sep + "deps")
        easy_install.main(["-U", "--install-dir " + livv.cwd + os.sep + "deps", "numpy"])
        
    # Show all of the dependency errors that were found
    if len(depErrors) > 0:
        print("Uh oh!")
        print("")
        print("Errors checking dependencies.  Errors found: ")
        for err in depErrors: print(err)
        exit(len(depErrors))
    else:
        print("Okay!")
     
def loadModules():
    FNULL = open(os.devnull, 'w')
    modules = ["ncl/6.1.0", "nco/4.3.9", "python_numpy/1.8.0", "python_matplotlib/1.3.1", "netcdf/4.1.3", "python_netcdf4/1.0.6"]
    for module in modules:
        p = subprocess.Popen("module load " + module, stdout=FNULL, stderr=FNULL, shell=True)
        if p != "":
            break
        else:
            print("Loading " + module + "....")


#
#
#
#
#
def installSetupTools():
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

        # Keep track of how much we have downloaded
        sizeOnDisk += len(buffer)
        f.write(buffer)
    os.system("python " + livv.cwd + os.sep + "deps" + os.sep + fileName + " --user")
        
def downloadJinja(tryNo):
    # If we've failed too many times quit
    if (tryNo > 4):
        depErrors.append("Too many failures trying to download & build Jinja2.  Try building manually before proceeding.  Exitting....")
        
    # Download Jinja2 tar
    url="https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.7.3.tar.gz#md5=b9dffd2f3b43d673802fe857c8445b1a"
    md5=url.split('=')[-1]
    fileName=url.split('/')[-1].split('#')[0]
    u = urllib2.urlopen(url)
    f = open(fileName, 'wb')
    urlInfo = u.info()
    fileSize = int(urlInfo.getheaders("Content-Length")[0])
    print("Downloading: " + fileName + " Size: " + str(fileSize))
    
    # Download it
    sizeOnDisk = 0
    block=8192
    while True:
        # We are downloading block by block - if we can't get anymore we must be done
        buffer = u.read(block)
        if not buffer: break

        # Keep track of how much we have downloaded
        sizeOnDisk += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (sizeOnDisk, sizeOnDisk * 100. / fileSize)
        status = status + chr(8)*(len(status)+1)
        print status,

    # Should be good to go, check the md5 as a precaution
    f.close()
    filemd5 = hashlib.md5(open(fileName, 'rb').read()).hexdigest()
    # If the checksum didn't go well try again (up to 5 times)
    if filemd5 != md5:
        print("Error downloading " + fileName + ".  Attempting download again.")
        downloadJinja(tryNo+1)
        
    jinjaDir = fileName.split(".tar")[0]
    tar = tarfile.open(fileName)
    if tarfile.is_tarfile(fileName):
        tar.extractall(".")
    installJinja = "python " + jinjaDir + os.sep + "setup.py install --user"
    os.system(installJinja)
    
    