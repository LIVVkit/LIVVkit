#!/usr/bin/env bash
# Copyright (c) 2015,2016, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

LIVV="../"
CURRENT="Copyright (c)"

ALWAYS_IGNORE=(-not -path "*.git*" -not -path "*docs/*" -not -iname "setup_*" -not -iname "MANIFEST.in")
PYTHON_IGNORE=(-not -iname "__init__.py" -not -iname "colormaps.py") 
CSS_IGNORE=(-not -iname "jquery-ui.min.css")

echo "--------------------------------------------------------------------------------"
echo "    PREPENDING A LICENSE HEADER ONTO THESE FILES:"
echo "--------------------------------------------------------------------------------"
find $LIVV -type f "${ALWAYS_IGNORE[@]}" \
    -not -iname "*.md" \
    -not -iname "*.json" \
    -not -iname "*.txt" \
    -not -iname "*.png" \
    -not -iname "*.jpg" \
    -not -iname "*.svg" \
    "${PYTHON_IGNORE[@]}" \
    "${CSS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | sort

echo "--------------------------------------------------------------------------------"
echo "    BEGIN PREPENDING:"
echo "--------------------------------------------------------------------------------"
#############################################################
## Prepend license header to python files without a shebang. 
## Will ignore files with a current license header. 
#############################################################
GET=( -iname "*.py" )

find $LIVV -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" "${PYTHON_IGNORE[@]}" \
    | xargs grep -L "#!" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-py /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done

#######################################################################
# Prepend license header to python, bash, and sh files with a shebang. 
# Will ignore files with a current license header. 
#######################################################################
GET=( -iname "*.py" -or -iname "*.sh" -or -iname "*.bash" )

find $LIVV -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" "${PYTHON_IGNORE[@]}" \
    | xargs grep -l "#!" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cat ${SRC} | head -1 > /tmp/licHead
    cat livvHeader-py >> /tmp/licHead
    cat ${SRC} | tail -n +2 >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done


####################################################
# Prepend license header to html files. 
# Will ignore files with a current license header. 
####################################################
GET=( -iname "*.html")

find $LIVV -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-html /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done

####################################################
# Prepend license header to css and js files. 
# Will ignore files with a current license header. 
####################################################
GET=( -iname "*.css" -or -iname "*.js" )

find $LIVV -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" "${CSS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-css /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done

####################################################
# Prepend license header to css files. 
# Will ignore files with a current license header. 
####################################################
GET=( -iname "*.ncl" )

find $LIVV -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-ncl /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    mv /tmp/licHead ${SRC}
done


echo "--------------------------------------------------------------------------------"
echo "    DONE PREPENDING!"
echo "--------------------------------------------------------------------------------"

