.. figure:: ./imgs/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Introduction
============
LIVVkit, the land ice verification & validation toolkit, is a python based V&V toolkit for
computational ice sheet models, in both a stand-alone or coupled (to an Earth system model)
configuration. It is intended to be a comprehensive testing suite that covers:

**Model V&V**

* Numerical verification -- "Are we solving the equations correctly?"
* Physical validation -- "Are we using the right physics?"

**Software V&V**

* Code verification  -- "did we build what *we* wanted?"
* Performance validation -- "did we build what the *users* wanted?"

LIVVkit easily integrates into a model's development workflow for regular and automated testing.
LIVVkit will help users and developers build confidence in their model results, and easily transmit
testing data to the wider scientific community, reviews, and decision/policy makers. 

Currently, LIVVkit is being developed and used in conjunction with the Community Ice Sheet Model
(`CISM <http://oceans11.lanl.gov/cism/documentation.html>`__), but is designed to be extensible to
other models.


User's Guide
============

.. toctree::
    :maxdepth: 2

    quickstart
    vv-intro
    design
    install
    usage
    faq
    dev

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
