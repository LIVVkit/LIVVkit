.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Quick Start
===========

Ready to jump right in?

.. note::

    All terminal (command line) commands in this document will be written POSIX compliant shells
    (``bash``, ``zsh``, ``fish``, etc.). The use of non-POSIX shells like ``csh`` is **not**
    recommended.


Basic Install
-------------

The latest LIVVkit release can be installed via `Python pip <https://pip.pypa.io/en/stable/>`__:

.. code-block:: bash

    pip install --user livvkit


LIVVkit was designed to be Python 2 and 3 compatible, so either Python version will work, but Python
3 is recommended. If you're having problems installing LIVVkit, see our :doc:`install` page, or
`open an issue on github <https://github.com/livvkit/livvkit/issues>`__.


Basic Usage
-----------

LIVVkit provides a command-line interface called ``livv``. To see the full list of options and verify
your installation, run:

.. code-block:: bash

    livv -h

Verification 
^^^^^^^^^^^^

In verification mode, LIVVkit analyzes and compares a regression testing dataset to a reference
dataset. For example, LIVVkit may analyze the dataset produced from a proposed CISM 2.0.6 release
(~400MB; `download here <http://jhkennedy.org/LIVVkit/cism-2.0.6-tests.20160728.tgz>`__)
and compare it to the dataset produced from the CISM 2.0.0 release
(~400MB; `download here <http://jhkennedy.org/LIVVkit/cism-2.0.0-tests.20160728.tgz>`__).
To run this example, first download the two aforementioned datasets to a directory, open a terminal,
and navigate to your download directory. Then, un-tar the datasets:

.. code-block:: bash

    tar -zxvf cism-2.0.0-tests.20160728.tgz
    tar -zxvf cism-2.0.6-tests.20160728.tgz

For ease, export the path to the two dataset directories:

.. code-block:: bash


    export REF=$PWD/cism-2.0.0-tests/titan-gnu/CISM_glissade
    export TEST=$PWD/cism-2.0.6-tests/titan-gnu/CISM_glissade

To run the suite use:

.. code-block:: bash
    
    livv --verify $TEST $REF --out-dir ver_test --serve

or more simply:

.. code-block:: bash
    
    livv -v $TEST $REF -o ver_test -s

LIVVkit will run the verification suite, report a summary of the results on the command line,
produce an output website in the created ``ver_test`` directory specified by the ``-o/--out-dir``
option, and launch a http server (the ``-s/--serve`` option) to easily view the output in your
favorite web browser.

.. note:: 

    LIVVkit will tell you the address to view the website at on the command
    line, which will typically look like
    `http://0.0.0.0:8000/ver_test/index.html <http://0.0.0.0:8000/ver_test/index.html>`__.


Viewing analyses
^^^^^^^^^^^^^^^^

Directly viewing the output websites (e.g., using ``file://`` addresses in a web browser) will likely not work
because most web browsers are disabling the use of local resources (e.g., javascript; see our :doc:`faq`).
Fortunately, The LIVVkit server can be used view any previously generated analyses. For example, to view
the ``ver_test`` analyses generated above again, simply specify the directory using the
``-o/--out-dir`` option and the ``-s/--serve`` option:

.. code-block:: bash

    livv -o ver_test -s


LIVVkit will then launch an HTTP server and tell you the address to view the website at on the
command line, which will typically look like
`http://0.0.0.0:8000/ver_test/index.html <http://0.0.0.0:8000/ver_test/index.html>`__.


Validation, Extensions
^^^^^^^^^^^^^^^^^^^^^^

LIVVkit is extensible to more in-depth or larger validation analyses. However, because these validation
analyses are particularly data intensive, many of the observational and example model output files are
much too large to distribute in the LIVVkit package. Therefore, we've developed a LIVVkit Extensions
repository (LEX) which uses `git-lfs <https://git-lfs.github.com>`__ (Git Large File Support) in order to
distribute the required data  [#]_. ``git-lfs`` can be installed either before or after
cloning this repository, but it will be needed *before* downloading the required
data. You can determine if you have ``git-lfs`` installed on your system by running
this command:

.. code:: bash

    command -v git-lfs


If ``git-lfs`` is not installed, you can install it by following the instructions here:

https://git-lfs.github.com

Once ``git-lfs`` is installed, clone and enter this repository:

.. code:: bash

    git lfs clone https://code.ornl.gov/LIVVkit/lex.git
    cd lex

.. warning::

    This repository is rather large (~ GBs currently).

Each extension will have an associated JSON configuration file which will describe
the extension's analysis code, data locations, and options. To see a list of
available extensions, you can run this command:

.. code:: bash

    find . -iname "*.json"

To execute any of these extensions, point ``livv``
to any of these extensions config file via the ``-e/--extension`` option (or the
``-V/--validate`` option). For example, to run the minimal example extension,
place the output website in the ``val_test`` directory, and serve the output website
you'd run this command:

.. code:: bash

    livv -e example/example.json -o vv_test -s


*Note:* All the extension configurations files assume you are working from the
top level ``lex`` directory. You *can* run any of these extensions from any
directory, but you will need to edit the paths in the JSON configuration files so
that ``livv`` can find the required files.

Likewise, you can also apply these analyses to any new model run [#]_ by adjusting
the paths to point to your model run.


Advanced
^^^^^^^^

Both the verification and validation commands can be executed at the same time and all results will
be placed into the same website. Additionally, you can pass the ``-V/validate`` option multiple
JSON configuration files, and it will run all of them. 

For more information, see :doc:`install`, :doc:`usage`, and :doc:`CONTRIBUTING`.


----------------------------------------------------------------------------------------------------

.. [#] You may find
   `this tutorial by Atlassian useful <https://www.atlassian.com/git/tutorials/git-lfs>`__.

.. [#] This assumes the new data files conform to the format of the included data
   files. That is, an extension that analyses output from the CISM-Albany ice
   sheet model will likely be able to analyze any similar CISM-Albany simulation,
   but likely would *not* be able to analyze output from the PISM ice sheet
   model without "massaging" the PISM files into a CISM-Albany like structure, or
   adjusting the extension. *This is a problem we are actively working on for future
   LEX releases.*
