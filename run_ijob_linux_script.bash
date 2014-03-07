#!/bin/bash

#created to automatically submit the ijob_linux files on a linux machine
#similar to what is at the end the master_build_$machine.csh scripts


export TEST_DIR=`pwd`

echo 
echo Running dome30 diagnostic test...
cd $TEST_DIR/reg_test/dome30/diagnostic
bash ijob_linux
echo ...done.
echo 
echo Running dome30 evolving test...
cd $TEST_DIR/reg_test/dome30/evolving
bash ijob_linux
echo ...done.
echo 
echo Running confined-shelf test...
cd $TEST_DIR/reg_test/confined-shelf
bash ijob_linux
echo ...done.
echo 
echo Running circular-shelf test...
cd $TEST_DIR/reg_test/circular-shelf
bash ijob_linux
echo ...done.
echo 
echo Running ismip-hom-a 80km test...
cd $TEST_DIR/reg_test/ismip-hom-a/80km
bash ijob_linux
echo ...done.
#echo 
#echo Running gis 10km test...
#cd $TEST_DIR/reg_test/gis_10km
#bash ijob_linux
#echo ...done.

