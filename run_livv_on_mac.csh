#!/bin/csh

echo "Running LIVV test suite on a Mac."
echo
echo "To run tests without rebuilding, use skip-build."
echo

@ skip_build_set = (($1 == skip-build) || ($2 == skip-build))
setenv QUICK_TEST nope
if (($1 == quick-test) || ($2 == quick-test)) then
  setenv QUICK_TEST quick-test
endif

#pushd . > /dev/null

if ($skip_build_set == 0) then
 cd ../../../builds/mac-gnu
 # csh mac-gnu-build-and-test-serial.csh no-copy skip-tests
 csh mac-gnu-build-and-test.csh $QUICK_TEST
 exit
endif

cd ../../../builds/mac-gnu
csh mac-gnu-build-and-test.csh skip-build no-copy $QUICK_TEST

#popd . > /dev/null
