Advanced installation
=====================


Latest release
--------------

The latest LIVVkit release can be installed via `Python pip <https://pip.pypa.io/en/stable/>`__:

.. code-block:: bash

    pip install --user livvkit

Via `Anaconda/Miniconda <https://conda.io/docs/download.html>`__: 

.. code-block:: bash

    conda install -c jhkennedy livvkit

Or by cloning the source from: 

.. code-block:: bash

    git clone https://github.com/LIVVkit/LIVVkit.git


LIVVkit was designed to be Python 2 and 3 compatible, so either version will work, but Python 3 is
recommended. If you're having problems installing LIVVkit, see our detailed :doc:`install` page, or
`open an issue on github <https://github.com/livvkit/livvkit/issues>`__.

For development
---------------

LIVVkit uses a public-private development model. The main development happens in a private
repository under the Department of Energy's  `ACME <https://github.com/ACME-climate>`_ project on
GitHub. The LIVVkit codebase is periodically released to public the `LIVVkit
<https://github.com/LIVVkit>`_ project on GitHub, and provided as a package on `PyPI
<https://pypi.python.org/pypi/livvkit>`_ and `Anaconda Cloud <https://anaconda.org/jhkennedy/livvkit>`_.

There are two encouraged ways to contribute to the development of LIVVkit:

1. For ACME developers
----------------------

First, contact `Joseph H. Kennedy <kennedyjh@ornl.gov>`_ and ask to be added to the
``ACME-Climate/LIVV`` repository. Once you have access to the repository, clone the code and
checkout the development branch:

.. code-block:: bash 
    
    git clone https://github.com/ACME-Climate/LIVV.git
    git checkout develop

When developing the code, please follow the `GitFlow workflow
<https://www.atlassian.com/git/tutorials/comparing-workflows#gitflow-workflow>`_ and make all your
changes in a feature branch. Feature branches should follow the ``username/feature`` naming
convention. 

If you have any questions, concerns, requests, etc., open an issue in our `private issues queue
<https://github.com/ACME-Climate/LIVV/issues>`_, and we will help you out. 

2. For non-ACME developers
--------------------------

Please use the `Forking Workflow
<https://www.atlassian.com/git/tutorials/comparing-workflows#forking-workflow>`_ to add
contributions to LIVVkit. 

First, go to the `LIVVkit github page <https://github.com/LIVVkit/LIVVkit>`_ and push the ``Fork``
button on the top right of the page. This will create a fork of LIVVkit in your profile page. Clone
the fork, make your changes, merge them to development branch, and then submit a pull request to our
public repository. 
   

If you have any questions, concerns, requests, etc., open an issue in our `public issues queue
<https://github.com/LIVVkit/LIVVkit/issues>`_, and we will help you out. 
