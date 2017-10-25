.. figure:: _static/livvkit.png
    :width: 400px
    :align: center
    :alt: LIVVkit

Frequently Asked Questions
==========================

Why is the output website blank? 
--------------------------------

Web browsers are disabling the use of local resources, like javascript, when viewing local files
(``file://``) due to possible security risks. As of writing this (2017/05/11), Firefox and Safari
will still display the output websites appropriately, but Chrome will not (IE/Edge untested), and
Firefox is slated to disable access in an upcoming release. 

Fortunately, there is an easy workaround! LIVVkit now has a ``-s/--serve SERVE`` option which will
fire up a local HTTP server, and serve the website over port ``SERVE`` (8000 is the default port).
LIVVkit will display the web address to view the website from; the default address will be
``http://localhost:8000/vv_YYYY-MM-DD/index.html`` where ``YYYY``, ``MM``, and ``DD`` are the
current year, month, and day, respectively.  


*Note, this will capture your terminal until you're done using the server (use* ``ctrl+c`` *to kill
it).* 

Alternatively, or for viewing previously generated websites, Python comes with a built in HTTP
server, which can be used to serve the website, and will run the javascript. First, move into the
output website directory (typically ``cd vv_YYYY_MM_DD``), and launch the server. Use either:

.. code:: sh

   python2 -m SimpleHTTPServer SERVE

or 

.. code:: sh

    python3 -m http.server SERVE

Where ``SERVE`` is port to serve the website over (8000 is the default port).

*Note, this will capture your terminal until you're done using the server (use* ``ctrl+c`` *to kill
it).* 

Now, open your favorite web browser and navigate to either ``http://localhost:8000/index.html`` or
``http://127.0.0.1:8000/index.html`` (adjust the port as necessary). You should now be able to see
the contents of the website.  When you rerun LIVVkit, you'll want to clear the browser's cache of
the output website when you reload the page. In most broswers, you can do that by using the
``ctrl+F5`` or ``ctrl+shit+R`` keyboard commands on Windows/Linux, or ``cmd+F5`` or ``cmd+shit+R``
on Mac.  

If you're still having problems, `open an issue on github
<https://github.com/livvkit/livvkit/issues>`__ and we'll help you out! 
