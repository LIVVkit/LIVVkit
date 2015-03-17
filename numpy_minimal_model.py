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

import numpy as np

