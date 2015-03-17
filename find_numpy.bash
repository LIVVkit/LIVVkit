#!/bin/bash

# a script to find all the times numpy is used. Once a specific python 
# file has been evaluated, if the usage is irrelevent, it will be 
# excluded from the find command.
find ./ -iname "*.py" \
    ! -name "numpy*model.py" \
    ! -name "livv.py" \
    ! -name "VV_depen*.py" \
    ! -name "VV_parser.py" \
    -exec grep --color=always -Hin "numpy" {} \;
