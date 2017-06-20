.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Extending Components
====================

Including New Models
--------------------
Adding new models requires a new implementation in the ``bundles`` directory.  Within the
``bundles`` directory there is a ``template`` directory that can be copied when adding compatibility
for a new model -- the name of the new directory should indicate the model being added (e.g.,
``cism_albany``, ``mpas_li``).  

.. warning::
    
    The bundle's name needs to follow the python naming convention for a python package (see
    :pep:`8#package-and-module-names`). 

The template directory provides sample modules with function stubs that can
be filled in to provide a drop in way to use each component (verification, performance, numerics,
and validation).  These functions primarily are used to accommodate for model-specific
implementations of things such as parsing log files, assimilating timing data, and arranging data
onto standard grids.

In addition to implementing component specific modules, each bundle must provide component level 
configuration files to provide information about which test cases are run, file and variable naming 
schemes, and data locations.

When the new bundle has been implemented and placed in the ``bundles`` directory it will 
automatically be registered by LIVVkit at runtime. It is important to note that in order to use 
LIVVkit on a new model it will also have to conform to the standards described in the 
:ref:`input-hierarchy` section (above).  

.. note:: 

    It is critical that the ``model_variant`` directory name is the same as the directory name that
    you have implemented in ``bundles``.


Adding Tests to Numerics or Validation
--------------------------------------
Inevitably the standard provided test cases provided by LIVVkit will not fit the needs of new 
scientific questions.  With this in mind, it is possible to add new sets of analyses into LIVVkit.  
We provide an extensible structure for the numerics and validation components, which are most likely
to change over time. Extending the software verification component, however, requires modifying the
component module itself. 

Like the implementation of new bundles we provide templates for each class of test that can be used
to extend LIVVkit to your analysis.  A new test consists of a configuration file and a Python module
that implements the ``run`` method, which takes a string and a dictionary as inputs.  These refer to 
the name of the test and the data extracted from the configuration file, respectively.  

Within the configuration file there is a required entry pointing to the module that contains the 
``run`` method described above.  It should be entered as you would import it from within Python 
itself.  In principle you can add the location of your module to your ``PYTHONPATH``, but the 
recommended method of including new analyses into LIVVkit is to either put them in the 
``components/validation_tests`` or ``components/numerics_tests`` or create a symlink to those 
locations.

When the analysis has been wrapped into these two files it can be run from the command line by 
providing the ``--validation`` argument followed by the path to the configuration file.


