.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Frequently Asked Questions
==========================

Why does the output website look weird and/or blank?
----------------------------------------------------

Web browsers are disabling the use of local resources, like javascript, when viewing local files
(``file://``) due to possible security risks. As of writing this (2017/05/11), Firefox and Safari
will still display the output websites appropriately, but Chrome will not (IE/Edge untested), and
Firefox is slated to disable access in an upcoming release. 

Fortunately, there is an easy workaround! LIVVkit now has a ``-s/--serve SERVE`` option which will
fire up a local HTTP server, and serve LIVVkit's output website over port ``SERVE`` (8000 is the default port).
This option can be used to immediately serve the output website once LIVVkit is finished running the
requested analyses, or to view a previously generated website. For example, to serve an output website
from the ``vv_test`` directory, you'd pass ``livv`` the ``-o/--out-dir`` and ``-s`` options:

.. code-block:: bash

    livv -o vv_test -s

LIVVkit will display the web address to view the website from; in this case the address will be
similar to ``http://localhost:8000/vv_test/index.html``.


*Note, this will capture your terminal until you're done using the server (use* ``ctrl+c`` *to kill
it).* 


If you're still having problems, `open an issue on github
<https://github.com/livvkit/livvkit/issues>`__ and we'll help you out! 
