#!/usr/bin/env bash
# Copyright (c) 2015-2017, UT-BATTELLE, LLC
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


# Get the source dir and ignore variables
source license-setup.sh

echo "--------------------------------------------------------------------------------"
echo "    PREPENDING A LICENSE HEADER ONTO THESE FILES:"
echo "--------------------------------------------------------------------------------"
find $SOURCE_DIR -type f "${ALWAYS_IGNORE[@]}" \
    "${FILE_IGNORE[@]}" \
    "${PYTHON_IGNORE[@]}" \
    "${JS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | sort

echo "--------------------------------------------------------------------------------"
echo "    BEGIN PREPENDING:"
echo "--------------------------------------------------------------------------------"
############################################################
# Prepend license header to python files without a shebang. 
# Will ignore files with a current license header. 
############################################################
GET=( -iname "*.py" )

find $SOURCE_DIR -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" "${PYTHON_IGNORE[@]}" \
    | xargs grep -L "#!" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-py /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    chmod --reference=${SRC} /tmp/licHead
    mv /tmp/licHead ${SRC}
done

#######################################################################
# Prepend license header to python, bash, and sh files with a shebang. 
# Will ignore files with a current license header. 
#######################################################################
GET=( -iname "*.py" -or -iname "*.sh" -or -iname "*.bash" )

find $SOURCE_DIR -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" "${PYTHON_IGNORE[@]}" \
    | xargs grep -l --max-count=1 "#!" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cat ${SRC} | head -1 > /tmp/licHead
    cat livvHeader-py >> /tmp/licHead
    cat ${SRC} | tail -n +2 >> /tmp/licHead
    chmod --reference=${SRC} /tmp/licHead
    mv /tmp/licHead ${SRC}
done


####################################################
# Prepend license header to js files. 
# Will ignore files with a current license header. 
####################################################
GET=(-iname "*.js" )

find $SOURCE_DIR -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" "${JS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-js /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    chmod --reference=${SRC} /tmp/licHead
    mv /tmp/licHead ${SRC}
done

####################################################
# Prepend license header to css files. 
# Will ignore files with a current license header. 
####################################################
GET=( -iname "*.ncl" )

find $SOURCE_DIR -type f \( "${GET[@]}" \) "${ALWAYS_IGNORE[@]}" \
    | xargs grep -L "$CURRENT" \
    | while read SRC 
do
    BN=`basename ${SRC}`
    echo HEADING ${SRC}
    cp livvHeader-ncl /tmp/licHead
    cat ${SRC} >> /tmp/licHead
    chmod --reference=${SRC} /tmp/licHead
    mv /tmp/licHead ${SRC}
done


echo "--------------------------------------------------------------------------------"
echo "    DONE PREPENDING!"
echo "--------------------------------------------------------------------------------"

