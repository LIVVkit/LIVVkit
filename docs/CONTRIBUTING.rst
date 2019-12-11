.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Contributing
############

LIVVkit is publicly developed within the `LIVVkit <https://github.com/LIVVkit>`_ project on GitHub
and releases are packaged and distributed on `PyPI <https://pypi.python.org/pypi/livvkit>`_ and
`Anaconda Cloud <https://anaconda.org/jhkennedy/livvkit>`_.


Workflow
--------

There are two encouraged ways to contribute to the development of LIVVkit:

1. Become a core developer
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have many contributions and are planning on being an active developer, you may request to
become a core developer by `opening an issue on github
<https://github.com/livvkit/livvkit/issues>`_ and briefly
describ your intended contribution goals. Once approved, you will be given push access to the
``LIVVkit/LIVVkit`` repository (and any other needed repositories). 

When developing the code, please follow the `GitFlow workflow
<https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow>`_ and make all your
changes in a feature branch. Feature branches should follow the ``#-username-feature`` naming
convention, where ``#`` indicates the issue  being addressed (optional). 

If you have any questions, concerns, requests, etc., open an issue in our `issues queue
<https://github.com/LIVVkit/LIVVkit/issues>`_, and we will help you out. 

2. For outside contributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For one-off or infrequent contributions, please use the `Forking Workflow
<https://www.atlassian.com/git/tutorials/comparing-workflows#forking-workflow>`_ to add
contributions to LIVVkit. 

First, go to the `LIVVkit github page <https://github.com/LIVVkit/LIVVkit>`_ and push the ``Fork``
button on the top right of the page. This will create a fork of LIVVkit in your profile page. Clone
the fork, make your changes, merge them to development branch, and then submit a pull request to our
public repository. 

If you have any questions, concerns, requests, etc., open an issue in our `public issues queue
<https://github.com/LIVVkit/LIVVkit/issues>`_, and we will help you out. 


Code Guidelines
---------------

LIVVkit 3.0+ will be developed and tested on the three latest Python versions (3.6--3.8 for LIVVkit 3.0).
Additionally, We generally follow `PEP 8 guidelines <https://www.python.org/dev/peps/pep-0008/>`__
as presented at `pep8.org <http://pep8.org/>`__, with the exception of line lengths:
lines have a soft limit of 100 characters and a hard limit of 120 characters when
extra length improves readability. We use the
`Google Style <https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings>`__
for our Docstrings. A sample code snippet below highlights most of our
coding conventions.

.. code-block:: python

    # coding=utf-8
    # LICENSE...

    """
    Description of module
    """

    import pymodule
    import pymodule2

    import livvmodule


    class ClassName(object):
        """
        Class descriptions
        """


        def __init__(self):
            """ Constructor """
            self.var = "value"
            self.auto = "nalue"
            self.bagger = "salue"
            self.autocrummify = "dalue"


        @functionAnnotation
        def foo(self, bar, baz):
            """
            A description of foo.

            Args:
                bar: What is this.
                baz: What is this.
            Returns:
                a combo of bar and baz
            """
            # Some extra logic
            return bar + baz



.. include:: README.rst
