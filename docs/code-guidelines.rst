Until `LIVVkit 3.0 <https://github.com/LIVVkit/LIVVkit/milestone/3>`__
is released, all code should be written as python 2 and 3 compatible
code -- see http://python-future.org/compatible_idioms.html.  Additionally, We
generally follow `PEP 8 guidelines <https://www.python.org/dev/peps/pep-0008/>`__
as presented at `pep8.org <http://pep8.org/>`__, with the exception of line lengths:
lines have a soft limit of 100 characters and a hard limit of 120 characters when
extra length improves readability.  See of a very nice presentation of the PEP 8
style guide.  A sample code snippet below highlights most of our
coding conventions.

.. literalinclude:: style.py
    :language: python

Tips
----

- Each source file containing functions that are called by the main ``livv.py`` script should have
  the license header. (There should be a script to fix when this is forgotten in util).
- Global variables should be stored in the module ``util.variables``.  When adding new global
  variables list them in that module with some basic default value so that it is easy for others to
  see which variables may be used by outside modules.
- When refering to system paths use the ``os.sep`` variable or ``os.path.join()`` instead of
  relying on whichever version of path separator your system uses.

