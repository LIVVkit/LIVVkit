.. figure:: _static/livvkit.png
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

License and Attribution 
-----------------------

LIVVkit |version| is an open source project licensed under a BSD 3-clause License. We ask that you
please acknowledge LIVVkit in any work it is used or supports, and in any corresponding published
work to please cite [Kennedy2017]_:

    Kennedy, J.H., et al. (2017), LIVVkit: An extensible, python-based, land ice
    verification and validation toolkit for ice sheet models, J. Adv. Model. Earth Syst., 9,
    `doi:10.1002/2017MS000916 <http://dx.doi.org/10.1002/2017MS000916>`__.

**Users and contributors are welcome!** We'll help you out --  `open an issue on github
<https://github.com/livvkit/livvkit/issues>`__ to contact us for any reason. 


User's Guide
============

.. toctree::
    :maxdepth: 3

    quickstart
    vv-intro
    design
    install
    usage
    extend
    dev
    api
    ref
    faq

Indices
=======

* :ref:`genindex`
* :ref:`modindex`

Search
======

* :ref:`search`
