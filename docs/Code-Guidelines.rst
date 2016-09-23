Conventions
~~~~~~~~~~~

A sample code snippet below highlights most of our coding conventions.
For conventions not covered in the snippet follow `PEP
guidelines <https://www.python.org/dev/peps/>`__.

.. code:: python

    # LICENSE #
    # HEADER #
    """
    Description of file
    """
    import pymodule
    import pymodule2

    import livvmodule

    class ClassName(Object):
        """
        Class descriptions
        """

        def __init__(self):
            """ Constructor """
            self.var          = "value"
            self.auto         = "nalue"
            self.bagger       = "salue"
            self.autocrummify = "dalue"


        @functionAnnotation
        def foo(bar, baz):
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

Tips
~~~~

- Each source file containing functions that are called by the main ``livv.py`` script should have
  the license header. (There should be a script to fix when this is forgotten in util).
- Global variables should be stored in the module ``util.variables``.  When adding new global
  variables list them in that module with some basic default value so that it is easy for others to
  see which variables may be used by outside modules.
- When refering to system paths use the ``os.sep`` variable or ``os.path.join()`` instead of
  relying on whichever version of path separator your system uses.

