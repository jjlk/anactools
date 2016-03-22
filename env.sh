#!/opt/local/bin/bash

### gamma directory
export GAMMALIB=$TOOLS/python/gamma
export CTOOLS=$TOOLS/python/gamma

### Path to data
#export VHEFITS=/Users/julien/Documents/WorkingDir/Tools/python/anactools/data/hess/prod/fits/prod_pa/pa_2015-07/Model_Deconvoluted_Prod26/Mpp_Std
export VHEFITS=/Users/julien/Documents/WorkingDir/Tools/python/anactools/data/hess/

### envs to work with gammalib/ctools
source $GAMMALIB/bin/gammalib-init.sh
source $CTOOLS/bin/ctools-init.sh

### To have access to analysis tools
export PYTHONPATH=$PYTHONPATH:$PWD/anactools

