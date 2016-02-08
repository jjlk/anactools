import sys
import os
import time

import gammalib
import ctools

import anactools.Utilities as Utilities
import anactools.ConfigHandler as ConfigHandler
from AnaTools import *
from PlotTools import *

"""
Do ctools analysis
Parameters:
-----------
configuration file
"""

### config file
if len(sys.argv) <2:
    print('param: configuration file')
    sys.exit()

configfile = sys.argv[1]
print sys.argv[1]

### open configuration file
try:
    cfg = ConfigHandler(configfile)
except:
    print('File not found: {0}'.format(configfile))
    sys.exit()

tstart = time.clock()

### Create output directory
outputdir = cfg.getValue('general','outputdir')
os.system('mkdir -p {0}'.format(outputdir))

#########################
### create model file ###
#########################
tstartmodel = time.clock()
try:
    Utilities.info('Generating xml file model...')
    ### HACK for now, waiting for csiasctobs to works
    #dealWithModelFile(cfg)
    Utilities.warning('Hack for the moment, waiting for csiactobs to handle H.E.S.S. data')
    print('Copying models/src_model.xml to outputdir/.')
    os.system('cp models/src_model.xml ' + outputdir + '/.')
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopmodel = time.clock()
print('==> OK (done in {0} s)'.format(tstopmodel-tstartmodel))

############################################
### handle data (skip this step for now) ###
############################################
tstartdata = time.clock()
try:
    Utilities.info('Handling data...')
    ### HACK for now, waiting for csiasctobs to works
    #handleData(cfg)
    Utilities.warning('Hack for the moment, waiting for csiactobs to handle H.E.S.S. data')
    print('Copying obs/obs.xml to outputdir/.')
    os.system('cp obs/obs.xml ' + outputdir + '/.')
except:
    pass
tstopdata = time.clock()
print('==> OK (done in {0} s)'.format(tstopdata-tstartdata))

###################
### select data ###
###################
tstartselect = time.clock()
#try:
Utilities.info('Selecting data...')
selectData(cfg)
#except:
 #   Utilities.warning('Problem ==> EXIT!')
  #  sys.exit()
tstopselect = time.clock()
print('==> OK (done in {0} s)'.format(tstopselect-tstartselect))

################
### bin data ###
################
tstartbin = time.clock()
try:
    Utilities.info('Binning data...')
    binData(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopbin = time.clock()
print('==> OK (done in {0} s)'.format(tstopbin-tstartbin))

#########################################
### make cubes(exposure, psf and bkg) ###
#########################################
tstartcubes = time.clock()
try:
    Utilities.info('Generating exposure, psf and bkg cubes...')
    makeCubes(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopcubes = time.clock()
print('==> OK (done in {0} s)'.format(tstopcubes-tstartcubes))

################
### make fit ###
################
tstartfit = time.clock()
try:
    Utilities.info('Minimizing...')
    makeFit(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopfit = time.clock()
print('==> OK (done in {0} s)'.format(tstopfit-tstartfit))


############################
### make spectral points ###
############################
tstartspec = time.clock()
spectrum = None
try:
    Utilities.info('Generating spectral points...')
    spectrum = makeSpectralPoints(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopspec = time.clock()
print('==> OK (done in {0} s)'.format(tstopspec-tstartspec))

if spectrum == None:
    Utilities.warning('Something\'s wrong with the spectrum object ==> EXIT!')
    sys.exit()
    
######################
### make butterfly ###
######################
tstartspec = time.clock()
try:
    Utilities.info('Generating butterfly...')
    makeButterfly(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopspec = time.clock()
print('==> OK (done in {0} s)'.format(tstopspec-tstartspec))


#####################
### plot spectrum ###
#####################
tstartplot = time.clock()
try:
    Utilities.info('Generating spectral plot...')
    showSpectrum(cfg, spectrum)
except:
    Utilities.warning('Problem ==> EXIT!')
    sys.exit()
tstopplot = time.clock()
print('==> OK (done in {0} s)'.format(tstopplot-tstartplot))


tend = time.clock()
print('\nJob done in {0} s'.format(tend-tstart))
