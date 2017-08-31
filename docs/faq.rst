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

Fortunately, there is an easy workaround! Python comes with a built in HTTP server, which can be
used to serve the website, and will run the javascript. First, move into the output website
directory (typically ``cd vv_$YEAR_$MONTH_$DAY``), and launch the server. Use either:

.. code:: sh

   python2 -m SimpleHTTPServer

or 

.. code:: sh

    python3 -m http.server

*Note, this will capture your terminal until you're done using the server (use* ``ctrl+c`` *to kill
it).* 

Now, open your favorite web browser and navigate to either ``http://localhost:8000/index.html`` or
``http://127.0.0.1:8000/index.html``. You should now be able to see the contents of the website.
When you rerun LIVVkit, you'll want to clear the browser's cache of the output website when you
reload the page. In most broswers, you can do that by using the ``ctrl+F5`` or ``ctrl+shit+R``
keyboard commands on Windows/Linux, or ``cmd+F5`` or ``cmd+shit+R`` on Mac.  

If you're still having problems, `open an issue on github
<https://github.com/livvkit/livvkit/issues>`__ and we'll help you out! 