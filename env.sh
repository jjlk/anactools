#!/opt/local/bin/bash

### gamma directory
export GAMMALIB=$TOOLS/gamma
export CTOOLS=$TOOLS/gamma

### Path to data
export VHEFITS=/Users/julien/Documents/WorkingDir/Tools/gamma/ana/data/hess/prod/fits/prod_pa/pa_2015-07/Model_Deconvoluted_Prod26/Mpp_Std/

### envs to work with gammalib/ctools
source $GAMMALIB/bin/gammalib-init.sh
source $CTOOLS/bin/ctools-init.sh

### To have access to analysis tools
export PYTHONPATH=$PYTHONPATH:$PWD/anactools

