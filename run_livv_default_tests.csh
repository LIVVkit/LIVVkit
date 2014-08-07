# script to run the default livv tests, called by the build-and-test scripts

if ($# < 4) then
 exit
endif
 

 setenv TEST_DIR $1
 setenv CISM_RUN_SCRIPT $2
 setenv PERF_TEST $3
 setenv CISM_VV_SCRIPT $4

 echo 'Submitting default LIVV test jobs to compute nodes.'

 setenv run_all_tests 1
 
 @ run_all_tests = ($5 != "quick-test")

 setenv RUN_TEXT qsub

 # should fix this hack:
 @ on_mac = 0
 if ($CISM_VV_SCRIPT == "mac_VV.bash") then
  @ on_mac = 1
  @ timeout_error = 0
  setenv RUN_TEXT " "
 endif
 echo $RUN_TEXT

 #diagnostic dome test case
 cd $TEST_DIR/reg_test/dome30/diagnostic
 $RUN_TEXT $CISM_RUN_SCRIPT


 if ($run_all_tests == 1) then

  #evolving dome test case
  cd $TEST_DIR/reg_test/dome30/evolving
  $RUN_TEXT $CISM_RUN_SCRIPT

  # confined shelf to periodic BC
  cd $TEST_DIR/reg_test/confined-shelf
  $RUN_TEXT $CISM_RUN_SCRIPT

  # circular shelf to periodic BC
  cd $TEST_DIR/reg_test/circular-shelf
  $RUN_TEXT $CISM_RUN_SCRIPT

  # ISMIP test case A, 80 km 
  cd $TEST_DIR/reg_test/ismip-hom-a/80km
  $RUN_TEXT $CISM_RUN_SCRIPT

  # ISMIP test case A, 20 km 
  cd $TEST_DIR/reg_test/ismip-hom-a/20km
  $RUN_TEXT $CISM_RUN_SCRIPT

  ## ISMIP test case C, 80 km - not operational for glide
  cd $TEST_DIR/reg_test/ismip-hom-c/80km
  $RUN_TEXT $CISM_RUN_SCRIPT
  
  ## ISMIP test case C, 20 km - not operational for glide
  cd $TEST_DIR/reg_test/ismip-hom-c/20km
  $RUN_TEXT $CISM_RUN_SCRIPT
 endif

  if ($PERF_TEST == 0 ) then
    echo "No performance suite jobs were submitted."
  else
    echo 'Submitting performance jobs to compute nodes.'
    echo 'Go to carver.nersc.gov to complete Visualization and Verification (LIVV)'

  #dome 60 test case
    cd $TEST_DIR/perf_test/dome60
    $RUN_TEXT $CISM_RUN_SCRIPT

  #dome 120 test case
    cd $TEST_DIR/perf_test/dome120
    $RUN_TEXT $CISM_RUN_SCRIPT

  #dome 240 test case
    cd $TEST_DIR/perf_test/dome240
    $RUN_TEXT $CISM_RUN_SCRIPT

  #dome 500 test case
    cd $TEST_DIR/perf_test/dome500
    $RUN_TEXT $CISM_RUN_SCRIPT

  #dome 1000 test case - not operational currently
  #  cd $TEST_DIR/perf_test/dome1000
  #  $RUN_TEXT $CISM_RUN_SCRIPT
  
  #gis 4km test case
  #  cd $TEST_DIR/perf_test/gis_4km
  #  $RUN_TEXT $CISM_RUN_SCRIPT
  
  #gis 2km test case
  #  cd $TEST_DIR/perf_test/gis_2km
  #  $RUN_TEXT $CISM_RUN_SCRIPT
  
  #gis 1km test case
  #  cd $TEST_DIR/perf_test/gis_1km
  #  $RUN_TEXT $CISM_RUN_SCRIPT
  endif
endif

set counter = 0
if ($on_mac == 0) then
 echo
 echo "Test Suite jobs started -- using qstat to monitor."
 echo 

 set still_running = 1
 #set counter = 0
 set timeout_error = 0

set run_list = "dome_30_test dome_30_evolve conf_shelf circ_shelf ishoma_20 ishoma_80 ishomc_20 ishomc_80 dome_60_test dome_120_test dome_240_test dome_500_test dome_1000_test"

 while ($still_running)
  set ls_out = `qstat | grep $USER`

  set found = 0 
  foreach cur ($run_list)
   foreach elem ($ls_out)
    if ("$cur" == "$elem") then
     if (($counter % 5) == 0) echo "Still running: $cur" 
     set found = 1
    endif
    # if ($found == 1) break 
   end 
  end
  if ($found == 0) then 
   echo "All jobs completed."
   set still_running = 0
  else 
   sleep 60
  endif
  @ counter = $counter + 1
  if ($counter == 120) then
   set still_running = 0
   set timeout_error = 1
   echo "Timeout error -- jobs are taking too long. Exiting script."
  endif
  if (($counter % 5) == 0) echo "Minutes: $counter"
 end
endif # on_mac == 0

 if ($timeout_error == 0) then
  echo "Total minutes: $counter"
  echo
 
  echo "Call disabled to: $CISM_VV_SCRIPT, which is located in:" 
  echo "$TEST_DIR/livv"
  echo
  echo "Perform this step on after the Test Suite jobs have completed."
  # cd $TEST_DIR/livv
  # bash $CISM_VV_SCRIPT from-script $1
 endif

 echo
 # echo "If there were errors finding ncl, add the ncl installation directory to your PATH in ~/.bashrc."
 echo
