#!/usr/bin/env bash

# Generates documentation for LIVVkit
#   run with ./generate_docs.sh

make distclean

sphinx-apidoc -f -o source/ ../livvkit/

ant -buildfile jsdoc-toolkit-rst-template/build.xml build
rm jsdoc-toolkit-rst-template/index.rst jsdoc-toolkit-rst-template/files.rst
sed -i 's/_global_ (data)/livvkit.resources.js.common module/g' jsdoc-toolkit-rst-template/symbols/_global_.rst

make html
