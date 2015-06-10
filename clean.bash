#!/bin/bash

#### clean up file from a livv run. Will destroy everything. ####


# remove compiled python files
find ./* -iname "*.pyc" -exec rm {} \;

# remove website
rm -r ./www
rm -r ./www_backup
