.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

This page provides a brief introduction to verification and validation (V&V) for scientific models
-- mostly to solidify the terminology we'll be using. We highly recommend reading our open access
publication in `JAMES
<http://agupubs.onlinelibrary.wiley.com/hub/journal/10.1002/(ISSN)1942-2466/>`__ for a detailed
discussion of V&V and its application in LIVVkit [Kennedy2017]_. For a very in depth discussion
of V&V for scientific computing, we recommend [Oberkampf2010]_.

Introduction to V&V
===================

Verification and validation (V&V) is a set of techniques that are used to build and quantify
confidence in *something*. That something can be a *numerical model* or a piece of *software*, and
building confidence in each of these will require the use of specialized techniques.

Model V&V
---------

Numerical models are typically used by scientists to make predictions about the physical world. V&V
of a numerical model consists of:

**Numerical verification** 
  The process of comparing the *approximate numerical* prediction against an *analytical*
  prediction, or in the case of a sufficiently complex problem, against highly accurate *community
  benchmark* solutions. This is inherently a **math** problem [Oberkampf2010]_ [Roache1998]_ that
  is represented by the question, "Are we solving the equations correctly?"

**Physical validation**
  The process of comparing the *numerical* predictions against *natural* phenomena. This is
  inherently a **physics** problem [Oberkampf2010]_ [Roache1998]_ that is represented by the
  question, "Are we using the right physics?"

Software V&V
------------

Software, on the other hand, is a *tool* made by a set of developers which is to be used for a set
of specific tasks by a *user*. V&V of a piece of software consists of:

**Code verification**
  The process of determining the software's implementation, and it's associated data, accurately
  represent the developers' specifications. This is inherently an **engineering** problem
  [Oberkampf2010]_ that is represented by the question, "did we build what *we* wanted?"

**Performance validation**
  The process of determining how *well* the software is able to be
  used for its intended task. This is inherently an **design** problem [Oberkampf2010]_ that is
  represented by the question, "did we build what the *users* wanted?"

Scientific model V&V
--------------------

Any *scientific model* (e.g., an ice sheet model) is a blend of the underlying numerical models used
to make the prediction, and the software that is used to drive the numerical models. Therefore,
validation and verification of any scientific model requires the use of both (numerical) model V&V
and software V&V. These two types of V&V techniques should be viewed as a complimentary process, as
the numerical and software code are intrinsically linked and live within the same code-base.

On confidence and credibility
-----------------------------

Confidence is (or at least should be) needed for *users* and *developers* to trust their modeling
and simulation (M&S) results, and to transmit them to the wider scientific community,
policy/decision makers, and other stakeholders. 

However, for those results to be *used* people outside the core user and development community, the
model must have an adequate level of credibility -- it much be trusted outside of the core
community. This is especially important when the results or predictions are used to inform policies
that may affect affect the economic and general well-being of citizens. 

Importantly, **confidence within the core community is not enough.** Credibility relies on the M&S
results being *reproducible*, the model being well-described and thoroughly tested, and all the
information relating to the development and testing of the model being *transparent* and easily
*discoverable* [Kennedy2017]_.
