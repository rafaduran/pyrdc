#!/bin/bash
TOOLS=`dirname $0`
VENV=$TOOLS/../.pyrdc-venv
source $VENV/bin/activate && $@
