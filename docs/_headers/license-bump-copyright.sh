#!/usr/bin/env bash
# Copyright (c) 2015-2018, UT-BATTELLE, LLC
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

OLD="Copyright (c) 2015-2018, UT"
NEW="Copyright (c) 2015-2018, UT"

echo "--------------------------------------------------------------------------------"
echo "    THESE FILES HAVE AN OUTDATED LICENSE HEADER:"
echo "--------------------------------------------------------------------------------"
find $SOURCE_DIR -type f "${ALWAYS_IGNORE[@]}" \
    "${FILE_IGNORE[@]}" \
    | xargs grep -l "$OLD" \
    | sort 

find ${SOURCE_DIR}/docs -type f \
    -not -path "*_build*" \
    -not -path "*source*" \
    "${FILE_IGNORE[@]}" \
    | xargs grep -l "$OLD" \
    | sort


echo "--------------------------------------------------------------------------------"
echo "    UPDATING THE LICENSE HEADERS:"
echo "--------------------------------------------------------------------------------"
find $SOURCE_DIR -type f "${ALWAYS_IGNORE[@]}" \
    "${FILE_IGNORE[@]}" \
    | xargs grep -l "$OLD" \
    | sort \
    | while read SRC 
do
    echo "Bumping $SRC"
    sed -i "s/$OLD/$NEW/g" $SRC
done


find ${SOURCE_DIR}/docs -type f \
    -not -path "*_build*" \
    -not -path "*source*" \
    "${FILE_IGNORE[@]}" \
    | xargs grep -l "$OLD" \
    | sort \
    | while read SRC 
do
    echo "Bumping $SRC"
    sed -i "s/$OLD/$NEW/g" $SRC
done

