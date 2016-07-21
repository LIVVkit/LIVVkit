.. image:: ./imgs/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Philosophy
==========

Verification and validation (V&V) is a set of techniques that are used
to quantify confidence and build credibility in *something*. That
something can be a *numerical model* or a piece of *software*, and
validating and verifying each of these requires the use of a different
set of techniques.

Model V&V
---------

Numerical models are typically used by scientists to make predictions
about the physical world. V&V of a numerical model consists of:

-  **Numerical verification** -- the process of comparing the
   *approximate numerical* prediction against an *analytical*
   prediction, or in the case of a sufficiently complex problem, against
   highly accurate *community benchmark* solutions. This is inherently a
   **math** problem `1,2 <VV#references>`__ that is represented by the
   question, "Are we solving the equations correctly?"

-  **Physical validation** -- the process of comparing the *numerical*
   predictions against *natural* phenomena. This is inherently a
   **physics** problem `1,2 <VV#references>`__ that is represented by
   the question, "Are we using the right physics?"

Software V&V
------------

Software, on the other hand, is a *tool* made by a set of developers
which is to be used for a set of specific tasks by a *user*. V&V of a
piece of software consists of:

-  **Code verification** -- the process of determining the software's
   implementation, and it's associated data, accurately represent the
   developers' specifications. This is inherently an **engineering**
   problem `2 <VV#references>`__ that is represented by the question,
   "did we build what *we* wanted?"

-  **Performance validation** -- the process of determining how *well*
   the software is able to be used for its intended task. This is
   inherently an **design** problem `2 <VV#references>`__ that is
   represented by the question, "did we build what the *users* wanted?"

Scientific model V&V
--------------------

Any *scientific model* (e.g., an ice sheet model) is a blend of the
underlying numerical models used to make the prediction, and the
software that is used to drive the numerical models. Therefore,
validation and verification of any scientific model requires the use of
both (numerical) model V&V and software V&V. These two types of V&V
techniques should be viewed as a complimentary process, as the numerical
and software code are intrinsically linked and live within the same
code-base.

References
----------

[1] Roache., P.J. (1998). Verification and Validation in Computational
Science and Engineering. Hermosa Publishers, Albuquerque, New Mexico.

[2] Oberkampf, W. L., & Roy, C. J. (2010). Verification and Validation
in Scientific Computing. Cambridge University Press.
