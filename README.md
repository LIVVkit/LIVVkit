![](https://github.com/ACME-Climate/LIVV/blob/develop/docs/livv.png)

===================================================================================================
  Land Ice Verification and Validation Toolkit
===================================================================================================
Last updated 4/17/2015
If this document is out of date send us an email!  See the contact section below for more details.


  Introduction
================
LIVV is a python-based toolkit for verification and validation of Ice Sheet Models.  LIVV provides a way for testing model output against a set of benchmark data.  Verification testing checks bitwise accuracy of solutions, and reports inconsistencies, as well as providing differences in configurations between model and benchmark data.  Standard output files are parsed for key information.  Validation and performance testing are under development.

For further documentation view the [wiki](https://github.com/ACME-Climate/LIVV/wiki)

  Before Using
================
Some requirements must be met before using LIVV.  LIVV was designed to be used with Python 2.7.  If you are using any other version of Python by default, use the command for Python 2.7 in place of any calls to `python` in this document (or any other LIVV Documentation).  If you are not sure what version of Python you are running try running `python --version` from a terminal.

LIVV depends on several software packages and libraries. We are working towards a completely automatic dependency management system, but some use cases may have been overlooked.  The complete list of dependencies for LIVV is as follows: 

 * Python 2.7
 * NetCDF 4.3.0+
 * NCO (NetCDF Operators) 4.4.0
 * HDF5 1.8.6
 * NCL (NCAR Command Language) 6.1.2
 * python-netCDF4
 * python-matplotlib
 * python-numpy
 * python-jinja2

If you are having any troubles with dependencies email us!  See the contact section below for more details.

 
  Obtaining Benchmark Data
============================
Send us an email to get a set of benchmark data.


  How to Use
==============
Using LIVV should be a painless experience.  You can give it a go with default settings simply by running:

> python livv.py

The default options will run all of the verification cases for the Dome, Ishom, and Shelf tests.  If you have a configuration with specific options that you have set up you can use:

> python livv.py -m CONFIG_NAME

To save your own configuration use:

> python livv.py [options] -m CONFIG_NAME -s

For a detailed list of options see the Options section, below.


  Options
===========
A variety of options can be used with LIVV.  A detailed list follows:

|	Option	| Description |
| ------------: | :-------------------------------------------------------------------------------------------------------------------------------- |
|  -h, --help |	Show the help message |
|  --dome=DOME | Specifies the Dome tests to run. |
|  --gis=GIS | Specifies the Greenland Ice Sheet tests to run					|
|  --ismip=ISMIP | Specifies the ismip tests to run								|
|  --shelf=SHELF | Specifies the shelf tests to run								|
|  --performance=PERF | Specifies the performance tests to run                      |
|  --comment=COMMENT |	Log a comment about this run									|
|  -o OUTPUTDIR, --outputDir=OUTPUTDIR | Location to output the LIVV webpages.							|
|  -i INPUTDIR, --inputDir=INPUTDIR | Location of the input for running tests.						|
|  -p PERFDIR, --performanceDir=PERFDIR | Location of the input for performance tests.                  |
|  -b BENCHDIR, --benchmarkDir=BENCHDIR | Location of the input for running tests.						|
|  -d DATADIR, --dataDir=DATADIR | Subdirectory where data is stored								|
|  -m MACHINE, --machine=MACHINE | Load a preconfigured set of options for a specific machine.		|
|  -s, --save |	Store the configuration being run with the given machine name.	|


  Contact
===========
Bug reports/Feature Requests:
  https://github.com/ACME-Climate/LIVV/issues

Andrew Bennett : 
  Github: arbennett
  Email:  bennettar@ornl.gov

Joseph Kennedy : 
  Github: jhkennedy
  Email:  kennedyjh@ornl.gov

Kate Evans : 
  Github: kevans32
  Email: evanskj@ornl.gov


TODO: A list of things that need to be updated.
-----------------------------------------------
 * Detail options more clearly
 * Give some use-cases (ie if the user wants to save a new configuration with a custom name)
 * Tell us what needs adding!
