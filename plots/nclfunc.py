"""
"""
import os
import subprocess

def plot_diff(var, testFile, benchFile, outFile):

    ncl_command = 'ncl \'bench = addfile("'+benchFile+'", "r")\' \'test = addfile("'+testFile+'", "r")\' \'plotFile = "'+outFile+'"\'  plots/vars/'+var+'_diff.ncl'

    # Be cautious about running subprocesses
    call = subprocess.Popen(ncl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdOut, stdErr = call.stdout.read(), call.stderr.read()

    if os.path.exists(outFile):
        print("    Bit4Bit plot details saved to "+outFile)
    else:
        print("****************************************************************************")
        print("*** Error saving "+outFile)
        print("*** Details of the error follow: ")
        print("")
        print(stdOut)
        print(stdErr)
        print("****************************************************************************")
