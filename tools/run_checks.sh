#!/bin/bash

wrapper=$1
#find rdc_crawler/ -name "*.py"

function clean {
    if [ -e pylint.txt ]; then
        rm pylint.txt
    fi
    if [ -e pep8.txt ]; then
        rm pep8.txt
    fi
}

function run_pylint {
  echo "Running pylint ..."
  PYLINT_INCLUDE="pyrdc"
  ${wrapper} pylint --rcfile=.pylintrc $PYLINT_INCLUDE > pylint.txt
}

function run_pep8 {
  echo "Running pep8 ..."
  PEP8_EXCLUDE=""
  PEP8_OPTIONS="--exclude=$PEP8_EXCLUDE --repeat"
  PEP8_INCLUDE="pyrdc/"
  echo "${wrapper} pep8 $PEP8_OPTIONS $PEP8_INCLUDE > pep8.txt"
  #${wrapper} pep8 $PEP8_OPTIONS $PEP8_INCLUDE > pep8.txt
  #perl string strips out the [ and ] characters
  ${wrapper} pep8 $PEP8_OPTIONS $PEP8_INCLUDE | perl -ple 's/: ([WE]\d+)/: [$1]/' > pep8.txt
}

clean
run_pylint
run_pep8
