#!/bin/bash

###########################################
# Prepend license header to python files. 
###########################################
for SRC in $(find ./ -name '*.py')
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-py /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done

#########################################
# Prepend license header to html files. 
#########################################
for SRC in $(find ./ -name '*.html')
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-html /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done

########################################
# Prepend license header to css files. 
########################################
for SRC in $(find ./ -name '*.css')
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-css /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done

