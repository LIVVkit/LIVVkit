.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Usage
#####

LIVVkit is intended to be integrated into a model's development cycle. A public-private version of
`GitFlow <https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow>`__ is a
common development cycle used by many scientific modeling groups, and LIVVkit would be integrated
into the development process like:

.. figure:: _static/workflow.png
    :width: 400px
    :align: center
    :alt: Development cycle

    Schematic of the public-private development cycle used by many scientfic modeling groups
    [Kennedy2017]_. A feature branch is created (``d124``, green path) from the current development
    branch (light purple path) and incremental changes are made (``f001``--``f003``). These changes
    frequently undergo the standard set of LIVVkit verification tests (dashed cyan circles). Once
    the feature is complete and tested (``f003``), it is ready to be merged into develop (which
    includes the new features ``d125``--``d126``) and a pull request will be opened by the developer
    (dashed arrow).  At this point, the integrators merge the feature into a local copy of the
    development branch and the full set of LIVVkit integration tests are started (filled cyan
    circle). Once passed, the feature is merged into develop (``d127``) and the pull request is
    closed. After enough features have been developed, the development branch will be merged into
    the private master branch (``m120``, right purple path), given a version tag (``v1.2.0``), and
    pushed to the mirrored master branch on the public repository (left purple path).


Standard verification and integration tests
===========================================

The standard verification and integration tests are performed by comparing a regression test
dataset, ``$TEST``, against a  reference dataset, ``$REF``. The datasets follows a somewhat rigid
leaf-node structure which allows the testing dataset to be more human-friendly than just a bunch of
files and still fully describe the tests. This directory structure is, for example, created by
CISM's Build and Test Structure (BATS).

.. _input-hierarchy:

Model Output/LIVVkit Input Hierarchy
------------------------------------

The directory layout of the model output should be as follows:

.. code-block:: bash

       BUNDLE
           ├── [METADATA]
           └── TEST
               ├── VARIANT
               │    ├── sRESO*
               │    │   ├── pPROC
               │    │   │   ├── [zSIZE*] 
               │    │   │   ├── ... 
               ...

where ``[]`` indicates an optional directory, ``BUNDLE`` indicate the specific ice-sheet model used
(including variant names; e.g., ``CISM_glissade``), ``METADATA`` indicates any directories that
contain information in addition to the testing data  (e.g., job submission scripts, CMakeCache.txt),
``TEST`` indicates a particular type of test (e.g., ``shelf``, ``dome``, ``ismip-hom``), ``VARIANT``
indicates any variant of that test (e.g., ``ismip-hom-a``), ``sRESO`` indicates the grid resolution,
``pPROC`` indicate the number of processors used to run the test, and ``zSIZE`` indicates the domain
size used in the test. 

.. note:: 

    The percise meaning of any ``*``-ed directory name may be variable from test to test, but
    will generally follow the definition given here. 


Standard verification  analysis
-------------------------------

The standard verification analysis typically compares a regression test dataset with a reference
dataset. Because these datasets can be quickly generated and analyzed (:math:`\Delta t \lesssim` a
coffee break), they can (and should) be run frequently. 

When a developer makes a new feature branch, they would first generate a reference dataset on their
development machine. 

For a CISM developer working on a Linux laptop/desktop, using the GNU compiler, and outputting the
datasets to a ``reg_ref`` directory, this would look like:

.. code-block:: bash

    cd $CISM
    git checkout -b feature-branch

    cd tests/regression/
    ./build_and_test.py -p linux-gnu -o reg_ref
    export REF=$PWD/reg_ref/linux-gnu/CISM_glissade

When a change is made to the model and the developer is ready to test their code, they
will then generate a test dataset on their development machine.

Again for a CISM developer working on a Linux laptop/desktop, using the GNU compiler, and outputting the
datasets to a ``reg_test`` directory, this would look like:

.. code-block:: bash

    # ... A change to CISM ...

    cd $CISM/tests/regression/
    ./build_and_test.py -p linux-gnu -o reg_test
    export TEST=$PWD/reg_test/linux-gnu/CISM_glissade

Then, the testing results can be compared to a reference dataset with LIVVkit: 

.. code-block:: bash
    
    cd $LIVV
    ./livv --verify $TEST $REF

LIVVkit will run the verification suite, report a summary of the results on the command line, and
produce an output website in the created ``vv_$YEAR_$MONTH_DAY`` directory  (or one specified with
the ``-o/--output`` option). The output website can be viewed in the developers preferred web
browser by by opening ``vv_$YEAR_$MONTH_DAY/index.html``. 

.. note:: 

    LIVVkit outputs the full path to the index page at the end of each run so it's easy type into the
    browser's address bar (prefix this path with a ``file://`` on most browsers).

.. warning:: 

    **Trouble viewing the output?** Your browser may have disabled javascript for local files (a
    security risk). See our :doc:`faq` for a work around. 

Once the feature is developed, and the developer is happy with the testing results, she/he would
push the feature branch to the development repository and open a pull request, kicking off a
integration analysis by the model integrator(s). Additionally, the output directory may
compressed and uploaded to Github for viewing by the integration team (every output website is
portable). 


Integration analysis
--------------------

Upon receiving a pull request for a new feature, a model's integration team will typically initiate
a more substantial test of the new feature, often on the target production machine(s). 

First, the integrator would checkout the code base on the production machine, and generate a
reference dataset for the current state of the development branch:

For a CISM integrator working on the supercomputer Titan at `OLCF <https://www.olcf.ornl.gov/>`__,
using the GNU compiler, and outputting the datasets to a ``reg_ref`` directory, this would look
like:

.. code-block:: bash

    cd $CISM
    git checkout develop

    cd tests/regression/
    ./build_and_test.py -b ref_build -p titan-gnu --timing -o reg_ref
    export REF=$PWD/reg_ref/linux-gnu/CISM_glissade

    cd reg_ref/titan-gnu/CISM_glissade
    ./submit-all-jobs.bash

.. note::

    For CISM, BATS recognizes a set of platforms that requires job sumission scripts,
    automatically sets up the jobs, and creates a submission script. Also, by specifying the
    ``--timing`` option, a much larger set of tests are run, including repeat runs for performance
    variability. 

Once those jobs are submitted, the integrator can attempt to merge in the feature branch. After all
conflicts are resolved, a test dataset would be generated.

Again, for a CISM integrator working on the supercomputer Titan at `OLCF
<https://www.olcf.ornl.gov/>`__, using the GNU compiler, and outputting the datasets to a
``reg_test`` directory, this would look like:

.. code-block:: bash

    cd $CISM
    git merge feature-branch

    # ... resolve any conflicts ...

    cd $CISM/tests/regression
    ./build_and_test.py -b test_build -p titan-gnu --timing -o reg_test
    export TEST=$PWD/reg_test/linux-gnu/CISM_glissade

    cd reg_test/titan-gnu/CISM_glissade
    ./submit-all-jobs.bash

Then once all the jobs were finished, the testing results can be compared to a reference dataset. 

.. code-block:: bash
    
    cd $LIVV
    ./livv --verify $TEST $REF

LIVVkit will run the verification suite, report a summary of the results on the command line, and
produce an output website in the created ``vv_$YEAR_$MONTH_DAY`` directory  (or one specified with
the ``-o/--output`` option). Because there is no web browser on Titan, the integrator would then
copy the output directory (and all contents) to their local machine and view the output website in the integrators
preferred web browser by by opening ``vv_$YEAR_$MONTH_DAY/index.html``. 

.. warning:: 

    **Trouble viewing the output?** Your browser may have disabled javascript for local files (a
    security risk). See our :doc:`faq` for a work around.

Additionally, the output directory may compressed and uploaded to Github for viewing by the rest of
the integration team and the feature developer (every output website is portable). If test results
aren't satisfactory, this provides a valuable resource for the developer to make the necessary
changes to their feature. 

Once testing results are satisfactory, the integration team may do a similar comparison to the
latest release in order to track changes over a longer period of development and analyze the model
for creep, or run a series of extended validation analyses. 

Extended validation analyses
----------------------------

.. note::
    
    A set of standard ice sheet model validation analyses are currently being developed and will be
    released soon (along with the ncessary observational data). Check back soon! Until then, see
    :doc:`extend` for how to develop your own validation analysis.



