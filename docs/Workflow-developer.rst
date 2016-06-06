Developers workflow
~~~~~~~~~~~~~~~~~~~

Using this workflow will allow you to perform a software `code
verification <VV-code-verification>`__ of model changes, and will
provide you with software `performance
validation <VV-performance-validation>`__ data of those changes.

Typically, this workflow will be used to compare the current state of a
model (``head`` of the development branch ``origin/develop``) with the
changes proposed in a pull request (``head`` of a feature banch
``user/feature``). Here the ``head`` of ``origin/develop`` will be the
benchmark commit, and the ``head`` of a ``user/feature`` will be the
test commit. More generally, this is just a comparison across two
commits, where the benchmark commit id is ``$ID_BENCH`` (``ID_BENCH`` is
an environment variable containing the commit id) and the test commit id
is ``$ID_TEST``. We will use the commit ids below.

There are 3 steps to the development workflow:

1. Build the benchmark and test versions of the model
2. Generate the benchmark and test data
3. Use LIVVkit to analyze the data

For this workflow, we will not assume that the benchmark data has
already been generated (unlike the `user-workflow <Workflow-user>`__).
However, for a comparison of ``origin/develop`` to ``user/feature``, the
benchmark data may already exist. In that case, the steps used to
generate the benchmark data can be skipped.

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

BATS is a relatively new feature and will only exist within recent
commits. We will first present a safe workflow, which does not assume
that BATS exists in either ``$ID_BENCH`` or ``$ID_TEST``. After the
presentation of the safe workflow, we will briefly present the quick
workflow, where BATS exists in both ``$ID_BENCH`` and ``$ID_TEST``.

The safe workflow
^^^^^^^^^^^^^^^^^

First, starting in a directory called ``$BASE``, clone three versions of
CISM, one will contain ``$ID_BENCH``, the second will contain
``$ID_TEST`` and the third will contain BATS. Then, checkout the needed
commits.

.. code:: sh

    git clone https://github.com/ACME-Climate/cism-piscees.git $BASE/cism-bench
    git clone https://github.com/ACME-Climate/cism-piscees.git $BASE/cism-test
    git clone https://github.com/ACME-Climate/cism-piscees.git $BASE/cism-bats

    cd $BASE/cism-bench
    git checkout -b bench $ID_BENCH

    cd $BASE/cism-test
    git checkout -b test $ID_TEST

    cd $BASE/cism-bats
    git checkout jhkennedy/regressions

Now, you can start building CISM and generating your data.

1. Build the benchmark version of CISM
''''''''''''''''''''''''''''''''''''''

Go to the benchmark version of CISM, and build CISM as you normally
would for your platform (``PLATFORM``) with your compiler of choice
(``COMPILER``). We use ``PLATFORM=titan`` and ``COMPILER=gnu`` for this
example. See the `BATS <build-and-test>`__ documentation for supported
platform and compiler combinations.

.. code:: sh

    cd $BASE/cism-bench/builds/titan-gnu/
    source titan-gnu-cmake
    make -j 8

Repeat the above for the test version of CISM.

.. code:: sh

    cd $BASE/cism-test/builds/titan-gnu/
    source titan-gnu-cmake
    make -j 8

Now you can generate the data.

2. Generating the benchmark and test data
'''''''''''''''''''''''''''''''''''''''''

Go to the BATS version of CISM, and generate the benchmark data.

.. code:: sh

    cd $BASE/cism-bats/tests/regression
    source setup_titan.bash
    ./build_and_test.py -p titan -c gnu --skip-build \
        -b $BASE/cism-bench/builds/titan-gnu \          # the benchmark build directory
        -o reg_bench \                                  # the benchmark data drectory
        --timing --performance

This will generate a ``reg_bench`` directory, which will contain a
``bash`` script to submit all the test runs. Submit the runs.

.. code:: sh

    cd reg_bench/titan-gnu/
    ./submit_all_jobs.bash | tee submit_all_jobs.log

Now, you can repeat the above procedure, substituting ``test`` for
``bench`` to generate the test data, as shown below.

.. code:: sh

    cd $BASE/cism-bats/tests/regression
    ./build_and_test.py -p titan -c gnu --skip-build \
        -b $BASE/cism-test/builds/titan-gnu \           # the test build directory
        -o reg_test \                                   # the test data directory
        --timing --performance

    cd reg_test/titan-gnu/
    ./submit_all_jobs.bash | tee submit_all_jobs.log

After all of your jobs have finished (job numbers will be found in the
two ``submit_all_jobs.log`` files), you will have a full set of
benchmark and test data for LIVVkit.

To see if you still have active running jobs, you can use the command

.. code:: sh

    showq -u USER

to see your current jobs, where ``USER`` is your user name on titan (or
hopper at NERSC). For more information on using a job submission queue,
see the users guide for your platform (`titans users
guide <https://www.olcf.ornl.gov/support/system-user-guides/titan-user-guide/>`__
and `hoppers users
guide <https://www.nersc.gov/users/computational-systems/hopper/>`__).

After all the jobs are run, you may clean out the un-needed files from
the timing directory by running the two ``clean_timing.bash`` scripts:

.. code:: sh

    cd $BASE/cism-bats/tests/regression/reg_bench/titan-gnu/
    ./clean_timing.bash

    cd $BASE/cism-bats/tests/regression/reg_test/titan-gnu/
    ./clean_timing.bash

This process can be repeated for any number of platform and compiler
combinations. The two ``reg_*`` directories with then contain a number
of ``PLATFORM-COMPILER`` data directories.

Note: If these steps are performed on a regular mac or linux personal
computer, ``./build_and_test.py`` will immediately run the jobs instead
of generating a job submission script and will automatically clean out
the timing directory once the timing runs have finished (if applicable).
If ``--performance`` and ``--timing`` are both specified, a very large
amount of tests will be run, and it will likely take a long time.
Neither need to be run, but without at least the ``--performance``
option specified, no performance validation data will be generated and
only code verification tests will be performed.

3. Use LIVVkit to analyze the data
''''''''''''''''''''''''''''''''''

Now that the benchmark and test data has been generated, you can run
LIVVkit. If you don't already have the LIVVkit code, clone a copy into
your ``$BASE`` directory.

.. code:: sh

    git clone https://github.com/ACME-Climate/LIVV.git $BASE/livv

Now, run LIVVkit.

.. code:: sh

    cd $BASE/livv
    git checkout develop
    source setup_titan.bash
    ./livv.py -o www_${ID_BENCH}-${ID_TEST} \                      # output website
        -b $BASE/cism-bats/tests/regression/reg_bench/titan-gnu/ \ # test data
        -t $BASE/cism-bats/tests/regression/reg_test/titan-gnu/  \ # benchmark data
        -c "Comparison of $ID_BENCH with $ID_TEST"
        --performance

The ``setup_titan.bash`` script represents the last known "good"
combination of modules that works with LIVVkit. You may need to adjust
as these type of platforms change frequently. (There is also a
``setup_hopper.bash``).

Once LIVVkit completes, you can look at the analysis in your preferred
internet browser.

.. code:: sh

    firefox www_${ID_BENCH}-${ID_TEST}/index.html

The can be repeated for any ``PLATFORM-COMPILER`` combinations that
exist within the ``reg_*`` directories. In fact, both the ``-b`` and
``-t`` options can be pointed to any BATS data directory -- you can even
do cross ``PLATFORM`` and/or ``COMPILER`` comparisons, or compare a
directory to itself. In the former case, bit-for-bit failures should be
*expected*, but the size of the differences and the performance
differences my be informative.

Note, this workflow can be simplified if BATS exists within the
benchmark, and test commit ids, as shown below.

The quick workflow
^^^^^^^^^^^^^^^^^^

Todo.

1. Build the benchmark version of CISM
''''''''''''''''''''''''''''''''''''''

Todo.

2. Generating the benchmark and test data
'''''''''''''''''''''''''''''''''''''''''

Todo.

3. Use LIVVkit to analyze the data
''''''''''''''''''''''''''''''''''

Todo.
