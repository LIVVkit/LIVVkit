.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Introduction
============
LIVVkit, the land ice verification & validation toolkit, is a Python based V&V toolkit for
computational ice sheet models, in both a stand-alone or coupled (to an Earth system model)
configuration. It is intended to be a comprehensive testing suite that covers:

**Model V&V**

* Numerical verification -- "Are we solving the equations correctly?"
* Physical validation -- "Are we using the right physics?"

**Software V&V**

* Code verification  -- "did we build what *we* wanted?"
* Performance validation -- "did we build what the *users* wanted?"

By integrating LIVVkit into a model's development workflow, LIVVkit will help users and developers
build confidence in their model results, and easily transmit testing data to the wider scientific
community, reviews, and decision/policy makers. 

Currently, LIVVkit is being used and developed in conjunction with E3SM
(`Energy Exascale Earth System Model <https://e3sm.org>`_) and CISM
(`Community Ice Sheet Model <https://cism.github.io/>`_), but is designed to be extensible to
other models.

**Users and contributors are welcome!** We'll help you out --  `open an issue on github
<https://github.com/livvkit/livvkit/issues>`_ to contact us for any reason.


License and Attribution 
-----------------------

LIVVkit |version| is an open source project licensed under a BSD 3-clause License. We ask that you
please acknowledge LIVVkit in any work it is used or supports. In any corresponding published
work, please cite [Kennedy2017]_ and [Evans2019]_:

    Evans, K. J., et al. (2019), LIVVkit 2.1: Automated and extensible ice sheet model validation,
    Geosci. Model Dev., 12, 1067–1086,
    `DOI:10.5194/gmd-12-1067-2019 <https://doi.org/10.5194/gmd-12-1067-2019>`_.

    Kennedy, J.H., et al. (2017), LIVVkit: An extensible, Python-based, land ice
    verification and validation toolkit for ice sheet models, J. Adv. Model. Earth Syst., 9,
    `DOI:10.1002/2017MS000916 <http://dx.doi.org/10.1002/2017MS000916>`_.


User's Guide
============

.. toctree::
    :maxdepth: 3

    quickstart
    vv-intro
    design
    install
    usage
    lex
    bundles
    CONTRIBUTING
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
