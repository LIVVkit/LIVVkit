![](https://raw.githubusercontent.com/wiki/LIVVkit/LIVVkit/imgs/livvkit.png)

===============================================================================
  Land Ice Verification and Validation Toolkit
===============================================================================

LIVVkit is a python-based toolkit for verification and validation of Ice Sheet
Models. It aims to provide the following capabilities:

**[Model V&V](https://github.com/LIVVkit/LIVVkit/wiki/VV)**
* Numerical verification -- "Are we solving the equations correctly?"
* Physical validation -- "Are we using the right physics?"

**[Software V&V](https://github.com/LIVVkit/LIVVkit/wiki/VV)**
* Code verification -- "did we build what *we* wanted?"
* Performance validation -- "did we build what the *users* wanted?"

Within LIVVkit, these capabilities are broken into four components:

Model V&V
* [Numerics](https://github.com/LIVVkit/LIVVkit/wiki/LIVVkit-numerics)
* [Validation](https://github.com/LIVVkit/LIVVkit/wiki/LIVVkit-validation)

Software V&V
[Verification](https://github.com/LIVVkit/LIVVkit/wiki/LIVVkit-verification)
[Performance](https://github.com/LIVVkit/LIVVkit/wiki/LIVVkit-performance)

Currently, LIVVkit is being developed and used in conjunction with the
Community Ice Sheet Model
([CISM](http://oceans11.lanl.gov/cism/documentation.html)), but is designed to
be extensible to other models. 

For further documentation view the 
[wiki](https://github.com/LIVVkit/LIVVkit/wiki).

  Before Using
================
### Install ###

Get a copy of LIVVkit by cloning this repo:

```sh
git clone https://github.com/LIVVkit/LIVVkit.git
```

LIVVkit was designed to be used with [Python 2.7](https://www.python.org/). If
you are using any other version of Python by default, use the command for
Python 2.7 in place of any calls to `python` in this document (or any other
LIVVkit Documentation).  If you are not sure what version of Python you are
running try running `python --version` from a terminal.

LIVVkit has some python package dependencies and some external package
dependencies. The required packages to use LIVVkit are:

Python Packages 
* [python-numpy](https://pypi.python.org/pypi/numpy/1.9.2) 
* [python-netCDF4](https://pypi.python.org/pypi/netCDF4) 
* [python-matplotlib](https://pypi.python.org/pypi/matplotlib/1.4.3)
* [python-jinja2](https://pypi.python.org/pypi/Jinja2/2.7.3) 

External Packages
[NetCDF 4.3.0+](http://www.unidata.ucar.edu/software/netcdf/)
[NCO (NetCDF Operators) 4.4.0](http://nco.sourceforge.net/)
[HDF5 1.8.6](https://www.hdfgroup.org/HDF5/)
[NCL (NCAR Command Language + graphics library) 6.1.2](http://www.ncl.ucar.edu/)

If you have a working install of CISM, you'll likely already have everything
you need besides [NCL](http://www.ncl.ucar.edu/), which you must install
manually.  LIVVkit will automatically install any missing python packages in
your `$HOME/.local` directory.

For more information about installing any of these dependencies, check the
links for each specific package. You may also be able to refer to the
installation instructions found in the
[CISM](http://oceans11.lanl.gov/cism/documentation.html) manual. 

If you are having any troubles with dependencies, open an issue on the 
[issue tracker](https://github.com/LIVVkit/LIVVkit/issues)!


  Usage
==========
LIVVkit is primarily controlled via options specified at the command line.
To see the full list of options, run:

```sh
./livv.py -h
```

or 

```sh
python livv.py -h
```

The are three main use cases for LIVVkit:
 
[User](https://github.com/LIVVkit/LIVVkit/Workflow-user) 
* verification of an install against a set of benchmark data 

[Developer](https://github.com/LIVVkit/LIVVkit/Workflow-developer) 
* verification and validation of model changes over time 

[Scientist](https://github.com/LIVVkit/LIVVkit/Workflow-scientist)
* validation of model results against observational and model generated data

Go to the above links to see their workflows. The 
[usage](https://github.com/LIVVkit/LIVVkit/Usage) 
page has a discussion of LIVVkit's options, advanced usage, and workflows. 


  Development 
===============

LIVVkit is currently under active development. See our 
[development roadmap](https://github.com/LIVVkit/LIVVkit/Development-roadmap). 

For feature request, questions, bug reporting, or other issues, use the 
[Issue Tracker](https://github.com/LIVVkit/LIVVkit/issues).

To contribute to LIVVkit, see: 
* <https://github.com/LIVVkit/LIVVkit/Contribute>

  Contact
===========

If you would like to suggest features, request tests, discuss contributions,
report bugs, ask questions, or contact us for any reason, use the
[Issue Tracker](https://github.com/LIVVkit/LIVVkit/issues).

Want to send us a private message?

**Andrew R. Bennett**
* github: @arbennett
* email: <a href="mailto:bennettar@ornl.gov">bennettar [at] ornl.gov</a>

**Joseph H. Kennedy** 
* github: @jhkennedy
* email: <a href="mailto:kennedyjh@ornl.gov">kennedyjh [at] ornl.gov</a>

**Katherine J. Evans** 
* github: @kevans32
* email: <a href="mailto:evanskj@ornl.gov">evanskj [at] ornl.gov</a>

If you're emailing us, we recommend CC-ing all three of us. 

