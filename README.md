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

Currently, LIVVkit is being used and developed in conjunction with E3SM
([Energy Exascale Earth System Model](https://e3sm.org/)) and CISM
([Community Ice Sheet Model](https://cism.github.io/)), but is designed
to be extensible to other models. For further documentation view the
[full documentation](https://livvkit.github.io/Docs).

**Users and contributors are welcome!** We’ll help you out –
[open an issue on github](https://github.com/LIVVkit/LIVVkit/issues)
to contact us for any reason.

  Installation 
================
The latest LIVVkit release can be installed via [pip](https://pip.pypa.io/en/stable/):

```sh
pip install livvkit
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

In verification mode, LIVVkit analyzes and compares a regression testing
dataset to a reference dataset. For example, LIVVkit may analyze the dataset
produced from a proposed CISM 2.0.6 release (~400MB; download
[here](http://jhkennedy.org/LIVVkit/cism-2.0.6-tests.20160728.tgz)) and
compare it to the dataset produced from the CISM 2.0.0 release (~400MB;
download [here](http://jhkennedy.org/LIVVkit/cism-2.0.0-tests.20160728.tgz)).
To run this example, first download the two aforementioned datasets to a
directory, open a terminal, and navigate to your download directory.
Then, un-tar the datasets:

```sh
tar -zxvf cism-2.0.0-tests.20160728.tgz
tar -zxvf cism-2.0.6-tests.20160728.tgz
```

For ease, export the path to the two dataset directories:

```sh
export REF=$PWD/cism-2.0.0-tests/titan-gnu/CISM_glissade
export TEST=$PWD/cism-2.0.6-tests/titan-gnu/CISM_glissade
```

To run the suite, use:

```sh
livv -v $TEST $REF -o cism206v200 -s
```

LIVVkit will run the verification suite, report a summary of the results
on the command line, produce an output website in the created `cism206v200`
directory specified by the `-o/--out-dir` option, and launch an http server
(the `-s/--serve option`) to easily view the output in your favorite web
browser. LIVVkit will tell you the address to view the website at on the
command line, which will typically look like
http://0.0.0.0:8000/ver_test/index.html.


 Validation, Extensions
-----------------------

LIVVkit is extensible to more in-depth or larger validation analyses.
However, because these validation analyses are particularly data intensive,
many of the observational and example model output files are much too
large to distribute in the LIVVkit package. Therefore, we've developed a
LIVVkit Extensions repository (LEX) which uses
[git-lfs](https://git-lfs.github.com) (Git Large File Support) in order to
distribute the required data. `git-lfs` can be installed either before or
after cloning this repository, but it will be needed *before* downloading
the required data. You can determine if you have `git-lfs` installed on
your system by running this command:

```sh
command -v git-lfs
```

If `git-lfs` is not installed, you can install it by following the instructions here:

https://git-lfs.github.com

Once `git-lfs` is installed, clone and enter this repository:

```sh
git lfs clone https://code.ornl.gov/LIVVkit/lex.git
cd lex
```

Each extension will have an associated JSON configuration file which will describe
the extension's analysis code, data locations, and options. To see a list of
available extensions, you can run this command:

```sh
find . -iname "*.json"
```

To execute any of these extensions, point `livv`
to any of these extensions config file via the `-e/--extension` option (or the
`-V/--validate` option). For example, to run the minimal example extension,
place the output website in the `val_test` directory, and serve the output website
you'd run this command:

```sh
livv -e example/example.json -o vv_test -s
```

*Note:* All the extension configurations files assume you are working from the
top level `lex` directory. You *can* run any of these extensions from any
directory, but you will need to edit the paths in the JSON configuration files so
that `livv` can find the required files.

Likewise, you can also apply these analyses to any new model run by adjusting
the paths to point to your model run.

 
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

