.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Installation
============


Basic
-----

The latest LIVVkit release can be installed via `Python pip <https://pip.pypa.io/en/stable/>`__:

.. code-block:: bash

    pip isntall --user livvkit

or `Anaconda/Miniconda <https://conda.io/docs/download.html>`__: 

.. code-block:: bash

    conda install -c conda-forge livvkit


LIVVkit was designed to be Python 2 and 3 compatible, so either version will work, but Python 3 is
preferred (and highly recommended). If you're having problems installing LIVVkit, try the advanced
installation below, and/or `open an issue on github <https://github.com/livvkit/livvkit/issues>`__.


Advanced
--------

In order to extend or contribute to LIVVkit, we recommend installing LIVVkit from the source code.
First, clone the source from GitHub: 

.. code-block:: bash

    git clone https://github.com/LIVVkit/LIVVkit.git


Then, you can install an "editable" version of LIVVkit into your python environment by: 

.. code-block:: bash

    cd LIVVkit
    pip install -e .

This will allow you to checkout different versions of LIVVkit, make changes, etc. and have those
changes immediately reflected in your python environment. 

LIVVkit was designed to be Python 2 and 3 compatible, so it should install into an environment using
either but Python 3 is preferred (and highly recommended). If you're having problems installing
LIVVkit, `open an issue on github <https://github.com/livvkit/livvkit/issues>`__.
