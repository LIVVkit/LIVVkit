.. image:: ./imgs/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Design
######

Repository Layout
=================
LIVVkit is designed to be as generic as possible, with an emphasis on providing basic 
infrastructure for performing V&V on models.  As a result LIVVkit's source code is broken into three
conceptual pieces:

 - **Components**: Provides modules for the four cases of analysis.  Numeric verification and model 
   validation contain separate test subdirectories for including specific pieces of analysis.

 - **Bundles**: Provides model specific implementations of various functions used in the standard 
   analysis sets.  Also provides the definitions for which sets of analysis should be run for each 
   specific model.

 - **Utilities**: Provides extra functionality that falls outside of the V&V paradigm.  This 
   includes classes and functions for accessing common data types, the rutime infrastructure (known 
   as the scheduler), and modules that facilitate IO.

In addition to these pieces LIVVkit provides some reference datasets used in included analyses and 
infrastructure for rendering output in the web browser.

Model Output/LIVVkit Input Hierarchy
====================================
LIVVkit's analysis are performed by finding files in a somewhat rigid structure.  The directory 
layout of the model output should be as follows:

.. code:: Python

       MODEL-Variant
           ├── metadata-etc
           └── run_name
               └── variant_name
                   ├── size_1
                   │   ├── processor_count_1
                   │   └── processor_count_2
                   └── size_2
                       └── processor_count_n


Extending Components
====================

Including New Models
--------------------
Adding new models requires a new implementation in the ``bundles`` directory.  Within the 
``bundles`` directory there should be a ``template`` directory that can be copied over when adding 
compatibility for a new model.  It provides sample modules with function stubs that can be filled in
to provide a drop in way to use each component (verification, performance, numerics, and 
validation).  These functions primarily are used to accomodate for model-specific implementations of things such 
as parsing log files, assimilating timing data, and arranging data onto standard grids.

In addition to implementing component specific modules, each bundle must provide component level 
configuration files to provide information about which test cases are run, file and variable naming 
schemes, and data locations.

When the new bundle has been implemented and placed in the ``bundles`` directory it will 
automatically be registered by LIVVkit at runtime. It is important to note that in order to use 
LIVVkit on a new model it will also have to conform to the standards described in the 
**Model Output/LIVVkit Input Hierarchy** section (above).  It is critial that the ``MODEL-Variant`` 
directory name is the same as the directory name that you have implemented in ``bundles``.  


Adding Tests to Numerics or Validation
--------------------------------------
Inevitably the standard provided test cases provided by LIVVkit will not fit the needs of new 
scientific questions.  With this in mind, it is possible to add new sets of analyses into LIVVkit.  
We limit these new tests to the numerics and validation components, although they can be any Python 
code in principle.

Like the implementation of new bundles we provide templates for each class of test that can be used
to extend LIVVkit to your analysis.  A new test consists of a configuration file and a Python module
that implements the ``run`` method that takes a string and a dictionary as inputs.  These refer to 
the name of the test and the data extracted from the configuration file, respectively.  

Within the configuration file there is a required entry pointing to the module that contains the 
``run`` method described above.  It should be entered as you would import it from within Python 
itself.  In principle you can add the location of your module to your ``PYTHONPATH``, but the 
reccommended method of including new analyses into LIVVkit is to either put them in the 
``components/validation_tests`` or ``components/numerics_tests`` or create a symlink to those 
locations.

When the analysis has been wrapped into these two files it can be run from the command line by 
providing the ``--validation`` argument followed by the path to the configuration file.

