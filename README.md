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
./livv.py -h
```

or 

```sh
python livv.py -h
```

For more information about using LIVVkit see the [documentation](https://livvkit.github.io/Docs)

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

