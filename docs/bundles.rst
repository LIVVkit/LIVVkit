.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Model Bundles
=============

.. warning::

    The model bundle abstraction is undergoing an overhaul (slated for LIVVkit 2.2) to make adding
    new models significantly easier. We are actively working on supporting
    MALI (`MPAS-Albany Land Ice <http://mpas-dev.github.io/land_ice/download.html>`_),
    PISM (`Parallel Ice Sheet Model <http://pism-docs.org/wiki/doku.php>`_),
    and others. If you'd like to help or request support for your model, please contact
    Joseph H. Kennedy at kennedyjh@ornl.gov.


Adding new models requires a new implementation in the ``bundles`` directory.  Currently, ``CISM_glissade``
is the only implemented bundle and it should be used as a template for a new bundle. Simply copy the
entire directory to a new directory where the name should indicate the model being added (e.g.,
``cism_albany``, ``mpas_li``).

.. warning::

    The bundle's name needs to follow the python naming convention for a python package (see
    :pep:`8#package-and-module-names`).

The new bundle will need to be edited for use each component (verification, performance, numerics,
and validation).  These functions primarily are used to accommodate for model-specific
implementations of things such as parsing log files, assimilating timing data, and arranging data
onto standard grids.

In addition to implementing component specific modules, each bundle must provide component level
configuration files to provide information about which test cases are run, file and variable naming
schemes, and data locations.

When the new bundle has been implemented and placed in the ``bundles`` directory it will
automatically be registered by LIVVkit at runtime. It is important to note that in order to use
LIVVkit on a new model it will also have to conform to the standards described in the
:ref:`input-hierarchy` section.

.. note::

    It is critical that the ``model_variant`` sub-directory in the LIVVkit input directory hierarchy
    name is the same as the directory name that you have implemented in ``bundles``.
