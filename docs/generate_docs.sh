#!/usr/bin/env bash

# Generates documentation for LIVVkit
#   run with ./generate_docs.sh

sphinx-apidoc -f -o source/ ../livvkit/

ant -buildfile jsdoc-toolkit-rst-template/build.xml build
cp jsdoc-toolkit-rst-template/symbols/_global_.rst source/js.rst

make html
