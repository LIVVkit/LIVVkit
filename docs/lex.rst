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
distribute the required data  [#]_. LEX holds a collection of  validation and custom analyses of ice
sheet models and their associated Earth system models.

LEX was first described in [Evans2019]_; to reproduce the analyses there, see the
`Reproducing Evans et al. (2019)`_ section.

    Evans, K. J., et al. (2019), LIVVkit 2.1: Automated and extensible ice sheet model validation,
    Geosci. Model Dev., 12, 1067–1086,
    `DOI:10.5194/gmd-12-1067-2019 <https://doi.org/10.5194/gmd-12-1067-2019>`_.


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

Reproducing Evans et al. (2019)
-------------------------------

If all the required `Dependencies`_ are installed, and you've cloned the repository
into the directory ``lex``, you can reproduce all the figures and tables in
[Evans2019]_ by running this command from within the ``lex`` directory:

.. code:: bash

    livv --validate smb/smb_icecores.json \
                    energy/energy_cesm.json \
                    clouds/clouds_cesm.json \
                    dynamics/dynamics_cisma.json \
                    -o vv_evans2018 -s

All the *model* data used for these analyses, and provided as an example, required some
postprocessing to generate the required input data for analysis with LIVVkit. A set of task-parallel
postprocessing scripts are provided in the ``postproc`` directory. While these scripts are
currently model specific, a new model can be adapted from current scripts using the directions in
the `postprocessing README <https://code.ornl.gov/LIVVkit/lex/blob/master/postproc/README.md>`__.
Note: A more generalized method of postprocessing model data is currently under development.

Developing a custom extension
-----------------------------

.. note::

    If you're thinking of developing a LIVVkit extension, open an issue on the
    `LIVVkit issue tracker <https://github.com/LIVVkit/LIVVkit/issues>`_ and
    we'll help you through the process.

A template extension is provided as an absolute minimum working example
in LEX's ``examples/`` directory. To start developing a new extension, copy the
``examples/template.*`` files to a (possibly new) relevant directory, and change
these files' name to a descriptive name. These files will provide the basis for your
new extension.

.. note::

    Importantly, the only things *required* for a new extension to run in LIVVkit
    is a ``run()`` method in a ``py`` file and an ``json`` config file as described
    below.

template.py:
^^^^^^^^^^^^

This is the primary extension Python module. In order to work with LIVVkit, the
extension needs to provide a ``run(name, config)`` function which accepts two arguments:
``name``, the name of the extension which will be displayed on the extensions output
webpage; and ``config`` which will contain the information in ``template.json``. This
function will then need to return a LIVVkit page element (:class:`livvkit.elements.elements.Page`)
which will contain a summary description of the extension (typically the extensions docstring),
and all the page elements to display (see :mod:`livvkit.elements`).


template.json:
^^^^^^^^^^^^^^

This file contains a JSON dictionary of the required input data for the extension. It
should minimally look like:

.. code:: json

    {
        "template" : {
            "module" : "examples/template.py",
            "references" : "examples/template.bib",
        }
    }

Where the path to the extension's module and extension's references are given.
When the paths are given as relative paths they will be taken as relative from the
top-level LEX directory, otherwise they should be given as absolute paths.

.. note::

    When developing an extension for *others*, at least data for a minimal working
    example should be contained in LEX and paths should be relative. If you're making
    an extension for *yourself* these can just be absolute paths to where the data
    lives on your machine.


Any other input data needed (e.g., parameters, flags, data file paths) for your
extension should be added here and not hard-coded ``template.py``.

template.bib:
^^^^^^^^^^^^^

The references that are relevant to this extension, and should be cited by anyone
using the extension to support any work that will be published. These references
will be displayed a the bottom of the extension's output webpage, and will include
[Kennedy2017]_ and [Evans2019]_ by default.


template.yml:
^^^^^^^^^^^^^

If you use any Python packages/modules beyond the required LIVVkit Python dependencies
(see LIVVkit's ``setup.py``), you should list them in this `Anaconda style environment
YAML file <https://conda.io/docs/user-guide/tasks/manage-environments.html?highlight=yml#create-env-file-manually>`__.
By doing so, when LIVVkit runs an extension in an environment without the required
dependencies, it will quit gracefully and suggest the Anaconda command which can
be used to install the dependencies.



Incorporating your extension into LEX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order for an extension to be accepted into LEX, the extension *must*:

#. Provide a summary description which describes the purpose of the extension,
   the data used, and any information needed for a clear contextual understanding
   of the analyses being presented.
#. Include a minimum working example dataset so that the extension can be tested,
   run, and understood immediately on any machine.
#. Include a ``.bib`` file and bibliography section that includes all relevant
   citations for the analyses being presented. *Please include a DOI where possible.*

For extensions that require data for which re-host permission cannot be granted,
they must include documentation on how to acquire and use the data as well as either
a small set of processed data or a set of "fake" example data.

Once you're extension is ready to add to LEX, please open an issue on the
`LIVVkit issue tracker <https://github.com/LIVVkit/LIVVkit/issues>`__ and we'll
help you get it integrated.


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
