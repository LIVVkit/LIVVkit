#!/bin/csh

echo "Running LIVV test suite on a Mac."
echo
echo "To run tests without rebuilding, use skip-build."
echo

@ skip_build_set = ($1 == skip-build)

#pushd . > /dev/null

if ($skip_build_set == 0) then
 cd ../../../builds/mac-gnu
 # csh mac-gnu-build-and-test-serial.csh no-copy skip-tests
 csh mac-gnu-build-and-test.csh
 exit
endif

cd ../../../builds/mac-gnu
csh mac-gnu-build-and-test.csh skip-build no-copy

#popd . > /dev/null
