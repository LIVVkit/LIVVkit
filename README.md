![](https://raw.githubusercontent.com/wiki/LIVVkit/LIVVkit/imgs/livvkit.png)

  The land ice verification and validation toolkit
===============================================================================

LIVVkit is a python-based toolkit for verification and validation of ice sheet
models. It aims to provide the following capabilities:

**Model V&V**
* Numerical verification -- "Are we solving the equations correctly?"
* Physical validation -- "Are we using the right physics?"

**Software V&V**
* Code verification -- "did we build what *we* intended?"
* Performance validation -- "did we build what the *users* wanted?"

Within LIVVkit, these capabilities are broken into four components:

Model V&V
* Numerics
* Validation

Software V&V
* Verification
* Performance

Currently, LIVVkit is being developed and used in conjunction with the
Community Ice Sheet Model
([CISM](http://oceans11.lanl.gov/cism/documentation.html)), but is designed to
be extensible to other models. 

For further documentation view the 
[full documentation](https://livvkit.github.io/Docs).

  Installation 
================
The latest LIVVkit release can be installed via [pip](https://pip.pypa.io/en/stable/):

```sh
pip install livvkit
```

or into a [conda](https://conda.io/docs/index.html) environment:

```sh
conda install -c jhkennedy livvkit
```

Additionally, LIVVkit is released on github, and you can clone the source code:

```sh
git clone https://github.com/LIVVkit/LIVVkit.git
```

If you are having any troubles with installation or dependencies, open an issue on the 
[issue tracker](https://github.com/LIVVkit/LIVVkit/issues) or contact us!


  Usage
==========
LIVVkit is primarily controlled via options specified at the command line.
To see the full list of options, run:

```sh
livv -h
```

 Verification
--------------

In verification mode, LIVVkit analyzes and compares a regression testing dataset to a reference
dataset, both of which are produced by CISM's built and test structure (BATS). For example, LIVVkit
may analyze the dataset produced from a proposed CISM 2.0.6 release
(~400MB; download [here](http://jhkennedy.org/LIVVkit/cism-2.0.6-tests.20160728.tgz)) 
and compare it to the dataset produced from the CISM 2.0.0 release 
(~400MB; download [here](http://jhkennedy.org/LIVVkit/cism-2.0.0-tests.20160728.tgz)).

```sh
export TEST=cism-2.0.6-tests/titan-gnu/CISM_glissade/
export REF=cism-2.0.0-tests/titan-gnu/CISM_glissade/

livv -v $TEST $REF -o cism206v200
```

This will produce a portable website in the `cism206v200` directory, which can be viewed by pointing
your preferred browser to `cism206v200/index.html`. 

*Note: recently we've been getting reports that Chrome will not display the javascript elements of
our output website when viewed on the local file system. If you're not seeing any elements on the
`cism206v200/index.html` page, try viewing with another browser (Firefox and Safari appear to be
working; IE untested).*

 Validation
------------

LIVVkit's validation option allows you to execute validation extensions (internal or external) by
pointing to one or more extension config file. LIVVkit ships with a extension template located in
`livvkit/components/validation_tests/template/`. If you don't know the location of `livvkit`, run
this command:

```sh
python -c 'import livvkit; print(livvkit.__file__)'
```

which will output something like: 

```sh
/home/joe/anaconda/envs/LIVVkit/lib/python3.6/site-packages/livvkit/__init__.py
```

Then, you can execute the extensions template like:

```sh
export LIVVKIT=/home/joe/anaconda/envs/LIVVkit/lib/python3.6/site-packages/livvkit

livv -V $LIVVKIT/components/validation_tests/template/template.json -o val_test
```

This will produce a portable website in the `val_test` directory, which can be viewed by pointing
your preferred browser to `val_test/index.html`. 

*Note: recently we've been getting reports that Chrome will not display the javascript elements of
our output website when viewed on the local file system. See our
[FAQ](https://livvkit.github.io/Docs/faq.html) for a work-around.  
 
 More
------

For more information about using LIVVkit see the [documentation](https://livvkit.github.io/Docs).

  Contact
===========

If you would like to suggest features, request tests, discuss contributions,
report bugs, ask questions, or contact us for any reason, use the
[Issue Tracker](https://github.com/LIVVkit/LIVVkit/issues).

Want to send us a private message?

**Joseph H. Kennedy** 
* github: @jhkennedy
* email: <a href="mailto:kennedyjh@ornl.gov">kennedyjh [at] ornl.gov</a>

**Katherine J. Evans** 
* github: @kevans32
* email: <a href="mailto:evanskj@ornl.gov">evanskj [at] ornl.gov</a>

If you're emailing us, we recommend CC-ing all of us. 

