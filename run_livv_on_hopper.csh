#!/bin/csh

echo "Running LIVV test suite on hopper."
echo

#pushd . > /dev/null
cd ../../../builds/hopper-gnu
csh hopper-gnu-build-and-test-serial.csh no-copy skip-tests
csh hopper-gnu-build-and-test.csh no-copy skip-tests
cd ../hopper-pgi
csh hopper-pgi-build-and-test.csh
#popd . > /dev/null
