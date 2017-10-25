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
    
    livv --verify $TEST $REF

or 

.. code-block:: bash
    
    livv -v $TEST $REF

LIVVkit will run the verification suite, report a summary of the results on the command line, and
produce an output website in the created ``vv_$YEAR_$MONTH_DAY`` directory (you can change the
output directory with the ``-o/--output`` option). You can view the output website by opening
``vv_$YEAR_$MONTH_DAY/index.html`` in your favorite web browser. 

.. note:: 

    LIVVkit outputs the full path to the index page at the end of each run so it's easy type into
    your browser's address bar (prefix this path with a ``file://`` on most browsers).

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

    livv --validate $LIVV/components/validation_tests/template/template.json 

or 

.. code-block:: bash

    livv -V $LIVV/components/validation_tests/template/template.json


LIVVkit will run the validation template, report a summary of the results on the command line, and
produce an output website in the created ``vv_$YEAR_$MONTH_DAY`` directory (you can change the
output directory with the ``-o/--output`` option). You can view the output website by opening
``vv_$YEAR_$MONTH_DAY/index.html`` in your favorite web browser.

.. note:: 

    LIVVkit outputs the full path to the index page at the end of each run so it's easy type into
    your browser's address bar (prefix this path with a ``file://`` on most browsers).

.. warning:: 

    **Trouble viewing the output?** Your browser may have disabled javascript for local files (a
    security risk). See our :doc:`faq` for a work around. 


Advanced
^^^^^^^^

Both the verification and validation commands can be executed at the same time and all results will
be placed into the same website. Additionally, you can pass the ``-V/validate`` option multiple
JSON configuration files, and it will run all of them. 

For more information, see :doc:`install`, :doc:`usage`, and :doc:`dev`. 
