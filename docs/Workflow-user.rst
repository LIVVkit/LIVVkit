Users workflow
~~~~~~~~~~~~~~

Using this workflow will allow you to perform a software `code
verification <VV-code-verification>`__ of a model installation.
Typically, this workflow will be used to build the latest model release,
and then evaluate that build against a developer-provided set of
benchmark data.

There are 3 steps to the development workflow:

1. Get the needed benchmark dataset
2. Build the latest versions of the model and generate the test dataset
3. Use LIVVkit to analyze the datasets

Note, LIVVkit is currently being developed and used in conjunction with
the Community Ice Sheet Model
(`CISM <http://oceans11.lanl.gov/cism/documentation.html>`__), and these
instruction are described for use with CISM. CISM includes a `build and
test structure (BATS) <Build-and-test>`__ which is capable of building
CISM and then using that build to generate a dataset for use with
LIVVkit. LIVVkit can be easily extended to other ice sheet models by
creating a BATS for it -- LIVVkit itself is model agnostic and only
analyzes the output data. Follow the link above for a detailed
description of BATS.

1. Getting the needed benchmark dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, starting in a directory called ``$BASE``, clone CISM and LIVVkit.

.. code:: sh

    cd $BASE
    git clone https://github.com/ACME-Climate/cism-piscees.git
    git clone https://github.com/ACME-Climate/LIVV.git

Benchmark datasets can be found at http://oceans11.lanl.gov/cism/livv/.
Here, you will find files named
``reg_bench.PLATFORM.CISM-VERSION.tar.gz`` that contain benchmark
datasets. You can use any of these benchmark datasets, but you should
use the one that *best matches your version of CISM and the platform you
are working on.*

Download the benchmark dataset and extract it in ``$BASE``. You will
then have a new directory called
``$BASE/reg_bench.PLATFORM.CISM-VERSION/``.

On some high performance computers (HPCs), such as titan at ORNL and
hopper at NERSC, the benchmark data will already be located there. You
can see if a dataset exists on your platform by looking in LIVVkit's
configurations directory:

.. code:: sh

    ls $BASE/LIVV/configurations/

Which will display a list of ``PLATFORM-COMPILER`` configuration files.
If a configuration file exists for your platform-compiler, the benchmark
dataset exists and that file will contain its location. This file will
be directly loaded into LIVVkit, and you need not open it to find the
location.

If a configuration is missing for your compiler, you can use one of the
alternate compiler files. If a configuration file is missing for your
platform, you will have to download the dataset that best matches your
platform from the location mentioned above. In both of these cases, you
should not expect bit-for-bit results, but you can still use the cross
platform/compiler comparison to get an idea of the relative level of
errors.

Now, you can start building CISM and generating your test dataset.

2. Build the latest version of CISM and generate the test dataset
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Go to BATS in your clone of CISM, and use BATS to build and generate
test dataset for your platform (``PLATFORM``) and compiler of choice
(``COMPILER``). We will use ``PLATFORM=titan`` and ``COMPILER=gnu`` for
this example. See the `BATS <build-and-test>`__ documentation for
supported platform and compiler combinations.

.. code:: sh

    cd $BASE/cism-piscees/tests/regression/
    source setup_titan.bash
    ./build_and_test.py -p titan -c gnu -o $BASE/reg_test

If you get the error message:

.. code:: sh

    ERROR: cannot find your cmake file:...

This means that your chosen platform and compiler combination doesn't
currently support out-of-source builds. BATS looks for a build script
called:

.. code:: sh

    $BASE/cism-piscees/builds/PLATFORM-COMPILER/PLATFORM-COMPILER-cmake.bash

which handles the out-of-source building. You will need to build CISM
manually, and then rerun BATS:

.. code:: sh

    cd $BASE/cism-piscees/builds/PLATFORM-COMPILER/
    source PLATFORM-COMPILER-cmake
    make -j 8
      
    cd $BASE/cism-piscees/tests/regression/
    source setup_titan.bash
    ./build_and_test.py -p titan -c gnu --skip-build \
        -b $BASE/cism-piscees/builds/PLATFORM-COMPILER/ \
        -o $BASE/reg_test

Once BATS successfully runs, it will generate a ``$BASE/reg_test``
directory, which will contain a ``bash`` script to submit all the test
runs. Submit the runs.

.. code:: sh

    cd $BASE/reg_test/titan-gnu/
    ./submit_all_jobs.bash | tee submit_all_jobs.log

After all of your jobs have finished (job numbers will be found in
``submit_all_jobs.log``), you will have a full set of benchmark and test
data for LIVVkit.

To see if you still have active running jobs, you can use the command

.. code:: sh

    showq -u USER

which will show your current jobs, where ``USER`` is your user name on
titan (or hopper at NERSC). For more information on using a job
submission queue, see the users guide for your platform (`titans users
guide <https://www.olcf.ornl.gov/support/system-user-guides/titan-user-guide/>`__
and `hoppers users
guide <https://www.nersc.gov/users/computational-systems/hopper/>`__).

Note: If these steps are performed on a regular mac or linux personal
computer, ``./build_and_test.py`` will immediately run the jobs instead
of generating a job submission script.

3. Use LIVVkit to analyze the data
''''''''''''''''''''''''''''''''''

Now that the benchmark and test data has been generated, you can run
LIVVkit:

-  If benchmark data exists on your platform:

.. code:: sh

    cd $BASE/LIVV
    source setup_titan.bash
    ./livv.py -t $BASE/reg_test/titan-gnu --load configurations/titan 

-  If you downloaded the benchmark data:

.. code:: sh

    cd $BASE/LIVV
    source setup_titan.bash
    ./livv.py -t $BASE/reg_test/titan-gnu -b $BASE/reg_bench.PLATFORM.CISM-VERSION/

The ``setup_titan.bash`` script represents the last known "good"
combination of modules that works with LIVVkit. You may need to adjust
as these type of platforms change frequently. (There is also a
``setup_hopper.bash``). This line can be omitted in the case of linux or
mac platforms.

Once LIVVkit completes, you can look at the analysis in your preferred
internet browser.

.. code:: sh

    firefox www/index.html
