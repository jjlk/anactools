import sys
import os
import time

import gammalib
import ctools

import anactools.Utilities as Utilities
import anactools.ConfigHandler as ConfigHandler
from anactools.AnaTools import *
from anactools.PlotTools import *

"""
Do ctools analysis
Parameters:
-----------
configuration file
"""

### config file
if len(sys.argv) < 2:
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
script_path = os.path.dirname(__file__)

### Create output directory
outputdir = cfg.getValue('general','outputdir')
os.system('mkdir -p {0}'.format(outputdir))

### Butterfly can be done only for pwl hypothesis (see why)
show_butterfly = True
if cfg.getValue('model','spectral') != 'pwl':
    show_butterfly = False

#########################
### create model file ###
#########################
tstartmodel = time.clock()
try:
    Utilities.info('Generating xml file model...')
    dealWithModelFile(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    raise
tstopmodel = time.clock()
print('==> OK (done in {0} s)'.format(tstopmodel-tstartmodel))

############################################
### handle data (skip this step for now) ###
############################################
tstartdata = time.clock()
try:
    Utilities.info('Handling data...')
    handleData(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    raise
tstopdata = time.clock()
print('==> OK (done in {0} s)'.format(tstopdata-tstartdata))

###################
### select data ###
###################
tstartselect = time.clock()
try:
    Utilities.info('Selecting data...')
    selectData(cfg)
except:
    Utilities.warning('Problem ==> EXIT!')
    raise
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
    raise
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
    raise
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
    raise
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
    raise
tstopspec = time.clock()
print('==> OK (done in {0} s)'.format(tstopspec-tstartspec))

if spectrum == None:
    Utilities.warning('Something\'s wrong with the spectrum object ==> EXIT!')
    sys.exit()
    
######################
### make butterfly ###
######################
if show_butterfly is True: 
    tstartspec = time.clock()
    try:
        Utilities.info('Generating butterfly...')
        makeButterfly(cfg)
    except:
        Utilities.warning('Problem ==> EXIT!')
        raise
    tstopspec = time.clock()
    print('==> OK (done in {0} s)'.format(tstopspec-tstartspec))
else:
    Utilities.info('Hypothesis is not pwl ==> No butterfly')

#####################
### plot spectrum ###
#####################
tstartplot = time.clock()
try:
    Utilities.info('Generating spectral plot...')
    showSpectrum(cfg, spectrum, show_butterfly)
except:
    Utilities.warning('Problem ==> EXIT!')
    raise
tstopplot = time.clock()
print('==> OK (done in {0} s)'.format(tstopplot-tstartplot))


tend = time.clock()
print('\nJob done in {0} s'.format(tend-tstart))

