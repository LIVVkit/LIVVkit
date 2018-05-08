.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Quick Start
===========

Ready to jump right in? 


Basic Install
-------------

The latest LIVVkit release can be installed via `Python pip <https://pip.pypa.io/en/stable/>`__:

.. code-block:: bash

    pip isntall --user livvkit

or `Anaconda/Miniconda <https://conda.io/docs/download.html>`__: 

.. code-block:: bash

    conda install -c jhkennedy livvkit


LIVVkit was designed to be Python 2 and 3 compatible, so either version will work, but Python 3 is
recommended. If you're having problems installing LIVVkit, see our :doc:`install` page, or
`open an issue on github <https://github.com/livvkit/livvkit/issues>`__.


Basic Usage
-----------

LIVVkit provides a command-line interface called ``livv``. To see the full list of options and verify
your installation, run:

.. code-block:: bash

    livv -h

Verification 
^^^^^^^^^^^^

To run the verification suite you will need a set of model *test* and *reference* data. Download
the example dataset (799 MB):

.. code-block:: bash
    
    wget jhkennedy.org/sites/default/files/LIVVkit/livvkit2.0.0_example_dataset.tar.gz
    tar -zxvf livvkit2.0.0_example_dataset.tar.gz

Then, for ease, export the path to the two dataset directories:

.. code-block:: bash

    cd livvkit2.0.0_example_dataset
    export REF=$PWD/cism-2.0.0-ref/titan-gnu/CISM_glissade
    export TEST=$PWD/cism-2.0.6-test/titan-gnu/CISM_glissade

To run the suite use:

.. code-block:: bash
    
    livv --verify $TEST $REF --out-dir ver_test --serve

or 

.. code-block:: bash
    
    livv -v $TEST $REF -o ver_test -s

LIVVkit will run the verification suite, report a summary of the results on the command line,
produce an output website in the created ``ver_test`` directory specified by the ``-o/--out-dir``
option, and launch a http server (the ``-s/--serve`` option) to easily view the output in your
favorite web browser.

.. note:: 

    LIVVkit will tell you the address to view the website at on the command
    line, which will typically look like
    `http://0.0.0.0:8000/ver_test/index.html <http://0.0.0.0:8000/ver_test/index.html>`_.

.. warning:: 

    **Trouble viewing the output?** Your browser may have disabled javascript for local files (a
    security risk). See our :doc:`faq` for a work around. 

Validation
^^^^^^^^^^

LIVVkit is extensible to more in-depth or larger validation analyses. A template validation module
is available To run a validation extension. First, find the location of LIVVkit on your system:

.. code-block:: bash

    export LIVV=$(dirname `python -c "import livvkit; print(livvkit.__file__)"`)
    echo $LIVV

Now, to run the validation template, pass the ``-V/--validate`` option the template extension's
configuration file (a JSON file). Use: 

.. code-block:: bash

    livv --validate $LIVV/components/validation_tests/template/template.json --out-dir val_test --serve

or 

.. code-block:: bash

    livv -V $LIVV/components/validation_tests/template/template.json -o val_test -s


LIVVkit will run the validation template, report a summary of the results on the command line,
produce an output website in the created ``val_test`` directory specified by the ``-o/--out-dir``
option, and launch a http server (the ``-s/--serve`` option) to easily view the output in your
favorite web browser.

.. note:: 

    LIVVkit will tell you the address to view the website at on the command
    line, which will typically look like
    `http://0.0.0.0:8000/val_test/index.html <http://0.0.0.0:8000/val_test/index.html>`_.

.. warning:: 

    **Trouble viewing the output?** Your browser may have disabled javascript for local files (a
    security risk). See our :doc:`faq` for a work around. 


Advanced
^^^^^^^^

Both the verification and validation commands can be executed at the same time and all results will
be placed into the same website. Additionally, you can pass the ``-V/validate`` option multiple
JSON configuration files, and it will run all of them. 

For more information, see :doc:`install`, :doc:`usage`, and :doc:`dev`. 
