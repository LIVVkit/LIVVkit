.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Installation
============


Basic
-----

The latest LIVVkit release can be installed via `Anaconda/Miniconda <https://conda.io/docs/download.html>`__
(preferred):

.. code-block:: bash

    conda install -c conda-forge livvkit

or `Python pip <https://pip.pypa.io/en/stable/>`__:

.. code-block:: bash

    pip isntall --user livvkit


LIVVkit 3.0 is being developed and tested against Python 3.6+, although earlier versions may work.
If you require Python 2, you may use LIVVkit 2, but it is no longer supported in conjunction with the
`Python 2 End of Life <https://www.python.org/doc/sunset-python-2/>`_.

If you're having problems installing LIVVkit, try the advanced installation below, and/or
`open an issue on github <https://github.com/livvkit/livvkit/issues>`__.


Advanced
--------

In order to extend or contribute to LIVVkit, we recommend installing LIVVkit from the source code.
First, clone the source from GitHub: 

.. code-block:: bash

    git clone https://github.com/LIVVkit/LIVVkit.git


Then, you can install an "editable" version of LIVVkit into a Python 3.6+ development environment by:

.. code-block:: bash

    cd LIVVkit
    pip install -e .[develop]

This will allow you to checkout different versions of LIVVkit, make changes, etc. and have those
changes immediately reflected in your Python environment.

If you're having problems installing/developing/using LIVVkit,
`open an issue on github <https://github.com/livvkit/livvkit/issues>`__.
