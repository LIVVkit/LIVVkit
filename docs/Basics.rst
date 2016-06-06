.. image:: ./imgs/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Getting Started
###############

Installation
============

To install LIVVkit via pip simply use:

.. code:: sh
    
    pip install livvkit

If you wish to get a copy of the source you can clone our Github repo:

.. code:: sh

    git clone https://github.com/LIVVkit/LIVVkit.git

You can then install LIVVkit with the `setup.py` script via:

.. code:: sh
    
    python setup.py

Or begin using LIVVkit directly from the cloned repository directory.

LIVVkit was designed to be used with `Python
XXX <https://www.python.org/>`__. If you are using any other version of
Python by default, use the command for Python XXX in place of any calls
to ``python`` in this document (or any other LIVVkit Documentation). If
you are not sure what version of Python you are running try running
``python --version`` from a terminal.

Dependencies
------------
LIVVkit's dependencies are listed below.  These packages are often 
available with `pip` or through your OS's package manager.  Links
to the packages on PyPI are here:

* `numpy <https://pypi.python.org/pypi/numpy>`_
* `matplotlib <https://pypi.python.org/pypi/matplotlib>`_
* `netCDF4 <https://pypi.python.org/pypi/netCDF4>`_

If you are having any troubles with dependencies, open an issue on the
`issue tracker <https://github.com/LIVVkit/LIVVkit/issues>`__!


Basic Usage
===========

LIVVkit can be controlled via options specified at the command
line. To see the full list of options, run:

.. code:: sh

    livv -h

after installing via `pip` or

.. code:: sh

    python /path/to/LIVVkit/livv -h

if you are running from a cloned repo.

To run the verification suite use:

.. code:: sh
    
    livv --verification path/to/model/data   path/to/benchmark/data

To run a validation suite use:

.. code:: sh

    livv --validation path/to/configuration/file

You can then view the output by opening the `index.html` file in the output 
directory with a web browser of your choosing.

