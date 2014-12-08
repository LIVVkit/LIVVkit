#!/bin/csh

echo "Running LIVV test suite on hopper."
echo
echo "To run tests without rebuilding, use skip-build."
echo

setenv CODE_DIR $HOME/cism-piscees

@ skip_build_set = ($1 == skip-build)

#pushd . > /dev/null

if ($skip_build_set == 0) then
 cd $CODE_DIR/builds/hopper-gnu
 csh hopper-gnu-build-and-test-serial.csh no-copy skip-build skip-tests 
 csh hopper-gnu-build-and-test.csh no-copy skip-build skip-tests 
 cd ../hopper-pgi
 csh hopper-pgi-build-and-test.csh skip-build no-copy
 exit
endif

cd $CODE_DIR/builds/hopper-pgi
csh hopper-pgi-build-and-test.csh skip-build no-copy

#popd . > /dev/null


