.. image:: ./imgs/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Design
######

Repository Layout
=================
LIVVkit is intended to provide a framework for ice-sheet model V&V and is designed to be as model
agnostic as possible.  As a result LIVVkit's source code is broken into three conceptual pieces:

 - **Components**: Provides modules for the four types of analysis (numerical verification, physical
   validation, code verification, and performance validation).  The numeric verification and physical 
   validation components contain a test subdirectories for including extended analyses.

 - **Bundles**: Provides any model specific functionality needed in the standard analysis sets. The
   Bundles also provide the list of analyses that should be run for each specific model.

 - **Utilities**: Provides extra functionality that falls outside of the V&V paradigm.  This 
   includes classes and functions for accessing common data types, the rutime infrastructure (known 
   as the scheduler), and modules that facilitate IO.

In addition to these pieces LIVVkit provides some reference datasets used in the included analyses and 
resources for rendering analysis output in the web browser.

Model Output/LIVVkit Input Hierarchy
====================================
LIVVkit's analyses are performed by finding files in a somewhat rigid structure.  The directory 
layout of the model output should be as follows:

.. code:: Python

       BUNDLE
           ├── [METADATA]
           └── TEST
               ├── VARIANT
               │    ├── sRESO*
               │    │   ├── pPROC
               │    │   │   ├── [zsize*] 
               │    │   │   ├── ... 
               ...

where ``[]`` indicates an optional directory, ``BUNDLE`` indicate the specific ice-sheet model used
(including variant names; e.g., ``CISM-glissade``), ``METADATA`` indicats any directories that contain
information inaddition to the testing data, ``TEST`` indicates a particular type of test (e.g., ``shelf``,
``dome``, ``ismip-hom``), ``VARIANT`` indicates any variant of that test (e.g., ``ismip-hom-a``), ``sRESO`` indicates
the grid resolution, ``pPROC`` indicate the number of processors used to run the test, and ``zSIZE``
indicates the domain size used in the test. *Note: The percise meaning of any* ``*`` *-ed directory name
may be variable from test to test, but will generally follow the definition given here.* 

Extending Components
====================

Including New Models
--------------------
Adding new models requires a new implementation in the ``bundles`` directory.  Within the
``bundles`` directory there is a ``template`` directory that can be copied when adding compatibility
for a new model -- the name of the new directory should indicat the model being added (e.g.,
``CISM-Albany``, ``MPAS-LI``).  The template directory provides sample modules with function stubs that can
be filled in to provide a drop in way to use each component (verification, performance, numerics,
and validation).  These functions primarily are used to accomodate for model-specific
implementations of things such as parsing log files, assimilating timing data, and arranging data
onto standard grids.

In addition to implementing component specific modules, each bundle must provide component level 
configuration files to provide information about which test cases are run, file and variable naming 
schemes, and data locations.

When the new bundle has been implemented and placed in the ``bundles`` directory it will 
automatically be registered by LIVVkit at runtime. It is important to note that in order to use 
LIVVkit on a new model it will also have to conform to the standards described in the 
`Model Output/LIVVkit Input Hierarchy`_ section (above).  
*Note: It is critial that the* ``MODEL-Variant`` 
*directory name is the same as the directory name that you have implemented in* ``bundles``.


Adding Tests to Numerics or Validation
--------------------------------------
Inevitably the standard provided test cases provided by LIVVkit will not fit the needs of new 
scientific questions.  With this in mind, it is possible to add new sets of analyses into LIVVkit.  
We provide an extensible structure for the numerics and validation components, which are most likely
to change over time. Exending the software verification component, however, requires modifying the
component module itself. 

Like the implementation of new bundles we provide templates for each class of test that can be used
to extend LIVVkit to your analysis.  A new test consists of a configuration file and a Python module
that implements the ``run`` method, which takes a string and a dictionary as inputs.  These refer to 
the name of the test and the data extracted from the configuration file, respectively.  

Within the configuration file there is a required entry pointing to the module that contains the 
``run`` method described above.  It should be entered as you would import it from within Python 
itself.  In principle you can add the location of your module to your ``PYTHONPATH``, but the 
reccommended method of including new analyses into LIVVkit is to either put them in the 
``components/validation_tests`` or ``components/numerics_tests`` or create a symlink to those 
locations.

When the analysis has been wrapped into these two files it can be run from the command line by 
providing the ``--validation`` argument followed by the path to the configuration file.

