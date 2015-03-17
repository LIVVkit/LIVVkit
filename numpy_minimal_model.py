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
diffFile2 = 'data/temp2.nc'
if not os.path.exists(modelFile):
    raise Exception("Can't find: "+modelFile)
if not os.path.exists(benchFile):
    raise Exception("Can't find: "+benchFile)


try:
    subprocess.check_call(['ncdiff', modelFile, benchFile, diffFile, '-O'])
    subprocess.check_call(['ncdiff', benchFile, modelFile, diffFile2, '-O'])
except (OSError, subprocess.CalledProcessError) as e:
    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
          + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
    try:
        exit(e.returncode)
    except AttributeError:
        exit(e.errno)


diffData = Dataset(diffFile, 'r')
diffVars = diffData.variables.keys()


print("Results from original calculations:")
print("-----------------------------------")
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
        print("Variable: thk")
        print("   Abs Difference: "+str(absDifference))
        print("   Max Difference: "+str(maxDifference))

# Check if any data in velnorm has changed, if it exists
if 'velnorm' in diffVars and diffData.variables['velnorm'].size != 0:
    data = diffData.variables['velnorm'][:]
    if data.any():
        absDifference += numpy.sum(numpy.ndarray.flatten(data))
        maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
        #plotVars.append('velnorm')
        change = 1
        print("Variable: velnorm")
        print("   Abs Difference: "+str(absDifference))
        print("   Max Difference: "+str(maxDifference))

# If there were any differences plot them out
if change:
    #self.plotDifferences(plotVars, modelFile, benchFile, diffFile)
    print("\nT'was a change.")
    print("   Abs difference: "+str(absDifference) )
    print("   Max difference: "+str(maxDifference) )
else:
    print("T'wasn't a change.")



diffData2 = Dataset(diffFile2, 'r')
diffVars2 = diffData2.variables.keys()

print("\n")
print("Results from switching ncdiff order:")
print("------------------------------------")
absDifference = 0.0
maxDifference = 0.0
plotVars = []
# Check if any data in thk has changed, if it exists
if 'thk' in diffVars2 and diffData2.variables['thk'].size != 0:
    data = diffData2.variables['thk'][:]
    if data.any():
        absDifference += numpy.sum(numpy.ndarray.flatten(data))
        maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
        #plotVars.append('thk')
        change = 1
        print("Variable: thk")
        print("   Abs Difference: "+str(absDifference))
        print("   Max Difference: "+str(maxDifference))

# Check if any data in velnorm has changed, if it exists
if 'velnorm' in diffVars2 and diffData2.variables['velnorm'].size != 0:
    data = diffData2.variables['velnorm'][:]
    if data.any():
        absDifference += numpy.sum(numpy.ndarray.flatten(data))
        maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
        #plotVars.append('velnorm')
        change = 1
        print("Variable: velnorm")
        print("   Abs Difference: "+str(absDifference))
        print("   Max Difference: "+str(maxDifference))

# If there were any differences plot them out
if change:
    #self.plotDifferences(plotVars, modelFile, benchFile, diffFile)
    print("\nT'was a change.")
    print("   Abs difference: "+str(absDifference) )
    print("   Max difference: "+str(maxDifference) )
else:
    print("T'wasn't a change.")



print("\n")
print("Results from new calculations:")
print("------------------------------")
absDifference = 0.0
maxDifference = 0.0
plotVars = []
# Check if any data in thk has changed, if it exists
if 'thk' in diffVars and diffData.variables['thk'].size != 0:
    data = diffData.variables['thk'][:]
    if data.any():
        absDifference += numpy.sum( numpy.absolute(numpy.ndarray.flatten(data)) )
        maxDifference = numpy.amax([ maxDifference, numpy.amax(numpy.absolute(data)) ])
        #plotVars.append('thk')
        change = 1
        print("Variable: thk")
        print("   Abs Difference: "+str(absDifference))
        print("   Max Difference: "+str(maxDifference))

# Check if any data in velnorm has changed, if it exists
if 'velnorm' in diffVars and diffData.variables['velnorm'].size != 0:
    data = diffData.variables['velnorm'][:]
    if data.any():
        absDifference += numpy.sum( numpy.absolute(numpy.ndarray.flatten(data)) )
        maxDifference = numpy.amax([ maxDifference, numpy.amax(numpy.absolute(data)) ])
        #plotVars.append('velnorm')
        change = 1
        print("Variable: velnorm")
        print("   Abs Difference: "+str(absDifference))
        print("   Max Difference: "+str(maxDifference))

# If there were any differences plot them out
if change:
    #self.plotDifferences(plotVars, modelFile, benchFile, diffFile)
    print("\nT'was a change.")
    print("   Abs difference: "+str(absDifference) )
    print("   Max difference: "+str(maxDifference) )
else:
    print("T'wasn't a change.")

diffData.close()
diffData2.close()
