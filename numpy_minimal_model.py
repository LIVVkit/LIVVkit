"""
numpy_minimal_model : A minimal model to test numpy.

The script is built to test numpy's handeling of large datasets and 
small errors when doing bit-for-bit tests. Currently, when the model 
results and the benchmark data are extreamely close, bit-for-bit fails
but LIVV can't:
    * plot the results
    * determine the maximum single point error

It seems errors that fall under 5e-7 return as zero with our datasets. 
However, in the python console, this code:
    >>> import numpy
    >>> a = numpy.array([5e-8, 5e-7, 5e-6])
    >>> numpy.amin(a)
    4.9999999999999998e-08

returns the expected result. Working theories:
    * Has to do with size of data? 
    * Some sort of type interaction with netCDF?

This is documented as issue #5 for LIVV. 
"""
import os
import sys
import subprocess
import numpy 

from netCDF4 import Dataset

modelFile = 'data/ishom.a.20km.JFNK.out.nc' 
benchFile = 'data/ishom.a.20km.JFNK.out_benchmark.nc'
diffFile  = 'data/temp.nc'

if not os.path.exists(modelFile):
    raise Exception("Can't find: "+modelFile)
if not os.path.exists(benchFile):
    raise Exception("Can't find: "+benchFile)


try:
    subprocess.check_call(['ncdiff', modelFile, benchFile, diffFile, '-O'])
except (OSError, subprocess.CalledProcessError) as e:
    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
          + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
    try:
        exit(e.returncode)
    except AttributeError:
        exit(e.errno)


diffData = Dataset(diffFile, 'r')
diffVars = diffData.variables.keys()

absDifference = 0.0
maxDifference = 0.0
plotVars = []
# Check if any data in thk has changed, if it exists
if 'thk' in diffVars and diffData.variables['thk'].size != 0:
    data = diffData.variables['thk'][:]
    if data.any():
        absDifference += numpy.sum(numpy.ndarray.flatten(data))
        maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
        #plotVars.append('thk')
        change = 1

# Check if any data in velnorm has changed, if it exists
if 'velnorm' in diffVars and diffData.variables['velnorm'].size != 0:
    data = diffData.variables['velnorm'][:]
    if data.any():
        absDifference += numpy.sum(numpy.ndarray.flatten(data))
        maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
        #plotVars.append('velnorm')
        change = 1

# If there were any differences plot them out
if change:
    #self.plotDifferences(plotVars, modelFile, benchFile, diffFile)
    print("T'was a change.")
    print("Absolute difference: "+str(absDifference) )
    print("Max difference:      "+str(maxDifference) )

diffData.close()
