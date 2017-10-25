#!/usr/bin/env bash

# Generates documentation for LIVVkit
#   run with ./generate_docs.sh


command -v jsdoc >/dev/null 2>&1 || { 
    printf "I require jsdoc but it's not installed. Install it like:\n"; 
    printf "  npm install -g jsdoc \nAborting.\n" >&2; 
    exit 1; 
}


make distclean

sphinx-apidoc -f -o source/ ../livvkit/

make html
