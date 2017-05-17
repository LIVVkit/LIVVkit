Building the documentation
==========================

To build this documentation use the ``generate_docs.sh`` script.  The generated website will be
output to ``_build/html``.  Before using it you will need to have some extra tools:

* ``sphinx``
* ``sphinx-api-any``
* ``jsdoc-toolkit``

The sphinx packages should be able to be installed via ``pip``. For ``jsdoc-toolkit``, download
http://jsdoc-toolkit.googlecode.com/files/jsdoc_toolkit-2.4.0.zip , extract it, and put the
``jsdoc-toolkit`` subdirectory into ``/opt``.


Thigs to do...

* generate autodocs
* generate jsdocs
* remove ``jsdoc-toolkit-rst-template/index.rst`` and ``jsdoc-toolkit-rst-template/files.rst``
* clean syntax in ``jsdoc-toolkit-rst-template/symbols/_global_.rst``
* change title in from ``_global_ (data)`` to ``livvkit.resources.js.common module``
* ``make html``

