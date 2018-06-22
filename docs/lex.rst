.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

LIVVkit Extensions (LEX)
========================

LIVVkit is extensible to more in-depth or larger validation analyses. However, because these validation
analyses are particularly data intensive, many of the observational and example model output files are
much too large to distribute in the LIVVkit package. Therefore, we've developed a LIVVkit Extensions
repository (LEX) which uses `git-lfs <https://git-lfs.github.com>`_ (Git Large File Support) in order to
distribute the required data  [#]_. LEX holds a collection of  validation and custom analyses of ice sheet models and their associated Earth
system models.

LEX was first described in [Evans2018]_; to reproduce the analyses there, see the
`Reproducing Evans et al. (2018)`_ section.

    Evans, K.J., J.H. Kennedy, D. Lu, M.M. Forrester, S. Price, J. Fyke,
    A.R. Bennett, M.J. Hoffman, I. Tezaur, C.S. Zender, and M. Vizcaino (In Review).
    LIVVkit 2.1: Automated and extensible ice sheet model validation.
    *Geoscientific Model Development.*

Dependencies
------------

Because Validation analyses are particularly data intensive, this extensions repo
uses `git-lfs <https://git-lfs.github.com>`_ (Git Large File Support) in order to
distribute the required data. ``git-lfs`` can be installed either before or after
cloning this repository, but it will be needed *before* downloading the required
data. You can determine if you have ``git-lfs`` installed on your system by running
this command:

.. code:: bash

    command -v git-lfs


If ``git-lfs`` is not installed, you can install it by following the instructions here:

https://git-lfs.github.com

Basic Usage
-----------

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

Reproducing Evans et al. (2018)
-------------------------------

If all the required `Dependencies`_ are installed, and you've cloned the repository
into the directory ``lex``, you can reproduce all the figures and tables in
[Evans2018]_ by running this command from within the ``lex`` directory:

.. code:: bash

    livv --validate smb/smb_icecores.json \
                    energy/energy_cesm.json \
                    clouds/clouds_cesm.json \
                    dynamics/dynamics_cisma.json \
                    -o vv_evans2018 -s



Developing a custom extension
-----------------------------

See the `LIVVkit documentation <https://livvkit.github.io/Docs/extend.html>`_ for
details on how to develop an extension. Briefly, a absolute minimum working example
is provided by the ``examples/`` extension, which should be copied to provide the
basis for your new extension. All extensions are required to contain a minimal working
example set of data such that they can be run an executed on any machine.

For extensions that require data for which re-host permission cannot be granted,
they must include documentation on how to acquire and use the data as well as either
a small set of processed data or a set of "fake" example data.


Issues, questions, comments, etc.?
----------------------------------

If you would like to suggest features, request tests, discuss contributions,
report bugs, ask questions, or contact us for any reason, use the
`LIVVkit issue tracker <https://github.com/LIVVkit/LIVVkit/issues>`_.

----------------------------------------------------------------------------------------------------

.. [#] You may find `this tutorial by Atlassian useful <https://www.atlassian.com/git/tutorials/git-lfs>`_.

.. [#] This assumes the new data files conform to the format of the included data
   files. That is, an extension that analyses output from the CISM-Albany ice
   sheet model will likely be able to analyze any similar CISM-Albany simulation,
   but likely would *not* be able to analyze output from the PISM ice sheet
   model without "massaging" the PISM files into a CISM-Albany like structure, or
   adjusting the extension. *This is a problem we are actively working on for future
   LEX releases.*
