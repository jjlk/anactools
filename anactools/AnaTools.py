import sys
import os
        
import gammalib
import ctools

import anactools.Utilities as Utilities
import anactools.ConfigHandler as ConfigHandler

def dealWithModelFile(cfg):
    """
    Import infos from configuration file and create a model file
    for the analysis
    """
    # Create model container
    models = gammalib.GModels()

    # coordinates
    src_dir = gammalib.GSkyDir()
    src_dir.radec_deg(cfg.getValue('model','coords','ra'),
                      cfg.getValue('model','coords','dec'))

    # spatial model
    spatial = None
    spectral = None
    opt_spatial = cfg.getValue('model','spatial')
    if opt_spatial == 'plike':
        spatial = gammalib.GModelSpatialPointSource(src_dir)
        spatial['RA'].min(-360.)
        spatial['RA'].max(360.)
        spatial['DEC'].min(-90.)
        spatial['DEC'].max(90.)
        if cfg.getValue('model','coords','fitposition') == True:
            spatial['RA'].free()
            spatial['DEC'].free()
        
    else: ## TODO
        pass

    # spectral model
    opt_spectral = cfg.getValue('model','spectral')
    if opt_spectral == 'pwl':
        spectral = gammalib.GModelSpectralPlaw()
        #print(spectral)
        ### fix prefactor
        prefactor = cfg.getValue('model','pwl','prefactor')
        spectral['Prefactor'].value(prefactor*1.e-17)
        #print(spectral)
        spectral['Prefactor'].min(1.e-24)
        spectral['Prefactor'].max(1.e-14)
        spectral['Prefactor'].scale(1.e-17)
        ### fix scale
        scale = cfg.getValue('model','pwl','scale')
        spectral['PivotEnergy'].value(scale*1.e6)
        spectral['PivotEnergy'].scale(1.e6)
        spectral['PivotEnergy'].min(1.e4)
        spectral['PivotEnergy'].max(1.e9)
        ### fix index
        index = cfg.getValue('model','pwl','index')
        #print index
        #print(spectral)
        spectral['Index'].value(index)
        spectral['Index'].scale(-1.)
        spectral['Index'].min(-0)
        spectral['Index'].max(-5)
    else: ## TODO
        pass

    model = gammalib.GModelSky(spatial, spectral)
    models.append(model)

    outputdir = cfg.getValue('general','outputdir')
    models.save(outputdir + '/' + cfg.getValue('model','output'))
    #print(models)
    del models

def handleData(cfg):
    Utilities.warning('Skipping this part for the moment!')
    
def selectData(cfg):
    """
    Select data with ctselect
    """
    outputdir = cfg.getValue('general','outputdir')
    select = ctools.ctselect()
    select["inobs"] = outputdir + '/' + cfg.getValue('csiactobs','obs_output')
    select["outobs"] = outputdir + '/' + cfg.getValue('ctselect','output')
    select["ra"] = cfg.getValue('model','coords','ra')
    select["dec"] = cfg.getValue('model','coords','dec')
    select["rad"] = cfg.getValue('ctselect','radius')
    select["emin"] = cfg.getValue('ctselect','emin')
    select["emax"] = cfg.getValue('ctselect','emax')
    select["tmin"] = cfg.getValue('ctselect','tmin')
    select["tmax"] = cfg.getValue('ctselect','tmax')
    select["usethres"] = cfg.getValue('ctselect','usethres')
    if cfg.getValue('general','debug') == True:
        select["debug"]    = True 

    #select["prefix"] = outputdir + '/' + 'selected_'
    select.run()
    select.save()

def binData(cfg):
    """
    bin data with ctbin
    """
    outputdir = cfg.getValue('general','outputdir')
    if cfg.getValue('general','anatype') == 'binned':
        bdata = ctools.ctbin()
        bdata["inobs"] = outputdir + '/' + cfg.getValue('ctselect','output')
        bdata["outcube"] = outputdir + '/' + cfg.getValue('ctbin','output')
        bdata["ebinalg"]  = "LOG"
        bdata["emin"]     = cfg.getValue('ctselect','emin')
        bdata["emax"]     = cfg.getValue('ctselect','emax')
        bdata["enumbins"] = cfg.getValue('ctbin','enumbins')
        bdata["nxpix"]    = cfg.getValue('ctbin','nxpix')
        bdata["nypix"]    = cfg.getValue('ctbin','nypix')
        bdata["binsz"]    = cfg.getValue('ctbin','binsz')
        bdata["coordsys"] = "CEL"
        bdata["proj"]     = "AIT"
        bdata["xref"]     = cfg.getValue('model','coords','ra')
        bdata["yref"]     = cfg.getValue('model','coords','dec')
        if cfg.getValue('general','debug') == True:
            bdata["debug"]    = True 
        bdata.run()
        bdata.save()

def makeCubes(cfg):
    """
    makes exposure, psf and bkg cubes
    """
    outputdir = cfg.getValue('general','outputdir')
    
    if cfg.getValue('general','anatype') == 'binned':
        ### create exposure map
        expcube = ctools.ctexpcube()
        expcube["inobs"] = outputdir + '/' + cfg.getValue('ctselect','output')
        expcube["incube"] = outputdir + '/' + cfg.getValue('ctbin','output')
        expcube["outcube"] = outputdir + '/' + cfg.getValue('ctexpcube','output')
        if cfg.getValue('general','edisp'): 
            like["edisp"]   = True
        
        expcube.run()
        expcube.save()
        
        ### create exposure map
        psfcube = ctools.ctpsfcube()
        psfcube["inobs"]   = outputdir + '/' + cfg.getValue('ctselect','output')
        psfcube["incube"]   = outputdir + '/' + cfg.getValue('ctbin','output')
        psfcube["outcube"]   = outputdir + '/' + cfg.getValue('ctpsfcube','output')
        if cfg.getValue('general','edisp'): 
            like["edisp"]   = True
        
        psfcube.run()
        psfcube.save()
        
        ### create background cube
        bkgcube = ctools.ctbkgcube()
        bkgcube["inobs"]   = outputdir + '/' + cfg.getValue('ctselect','output')
        bkgcube["inmodel"]   = outputdir + '/' + cfg.getValue('csiactobs','model_output')
        bkgcube["incube"]   = outputdir + '/' + cfg.getValue('ctbin','output')
        bkgcube["outcube"]   = outputdir + '/' + cfg.getValue('ctbkgcube','output_cube')
        bkgcube["outmodel"]   = outputdir + '/' + cfg.getValue('ctbkgcube','output_model')
        bkgcube["debug"]    = True
        bkgcube["chatter"]    = 4
        bkgcube.run()
        bkgcube.save()    

def makeFit(cfg):
    """
    makes fit with ctlike
    """
    # Perform maximum likelihood fitting
    outputdir = cfg.getValue('general','outputdir')
    
    like = ctools.ctlike()
    if cfg.getValue('general','anatype') == 'unbinned':
        like["inobs"] = outputdir + '/' + cfg.getValue('ctselect','output')
        like["inmodel"] = outputdir + '/' + cfg.getValue('csiactobs','model_output')
    elif cfg.getValue('general','anatype') == 'binned':
        like["inobs"] = outputdir + '/' + cfg.getValue('ctbin','output')
        like["inmodel"] = outputdir + '/' + cfg.getValue('ctbkgcube','output_model')
        like["expcube"]   = outputdir + '/' + cfg.getValue('ctexpcube','output')
        like["psfcube"]   = outputdir + '/' + cfg.getValue('ctpsfcube','output')
        like["bkgcube"]   = outputdir + '/' + cfg.getValue('ctbkgcube','output_cube')
    else:
        Utilities.warning('Unlnown type: {}'.format(cfg.getValue('general','anatype')))
        sys.exit()
        
    if cfg.getValue('general','edisp'): 
        like["edisp"]   = True
    else:
        like["edisp"]   = False
        
    like["outmodel"] = outputdir + '/' + cfg.getValue('ctlike','output')
    like["chatter"] = 1
    if cfg.getValue('general','debug') == True:
        like["debug"]    = True 

    like.run()
    like.save()  

import cscripts
    
def makeSpectralPoints(cfg):
    """
    Computes spectrum
    """
    outputdir = cfg.getValue('general','outputdir')
    
    spec = cscripts.csspec()
    if cfg.getValue('general','anatype') == 'unbinned':
        spec["inobs"] = outputdir + '/' + cfg.getValue('ctselect','output')
        spec["inmodel"] = outputdir + '/' + cfg.getValue('ctlike','output')
    elif cfg.getValue('general','anatype') == 'binned':
        spec["inobs"] = outputdir + '/' + cfg.getValue('ctbin','output')
        spec["inmodel"] = outputdir + '/' + cfg.getValue('ctlike','output')
        spec["expcube"]   = outputdir + '/' + cfg.getValue('ctexpcube','output')
        spec["psfcube"]   = outputdir + '/' + cfg.getValue('ctpsfcube','output')
        spec["bkgcube"]   = outputdir + '/' + cfg.getValue('ctbkgcube','output_cube')
    else:
        Utilities.warning('Unknown type: {}'.format(cfg.getValue('general','anatype')))
        sys.exit()
        
    spec["outfile"] = outputdir + '/' + cfg.getValue('csspec','output')
    spec["emin"] = cfg.getValue('csspec','emin')
    spec["emax"] = cfg.getValue('csspec','emax')
    spec["enumbins"] = cfg.getValue('csspec','enumbins')
    spec["srcname"] = ""
    spec["ebinalg"] = "LOG"
    if cfg.getValue('general','edisp'): 
        spec["edisp"]   = True
    else:
        spec["edisp"]   = True
    if cfg.getValue('general','debug') == True:
        spec["debug"]    = True

    #spec.run()
    spec.execute()  

    ### make copy of spectrum
    spectrum = spec.spectrum().copy()
    return spectrum

def makeButterfly(cfg):
    """
    Computes butterfly (only for power law, fix in the future?)
    """
    outputdir = cfg.getValue('general','outputdir')
    
    butt = ctools.ctbutterfly()
    if cfg.getValue('general','anatype') == 'unbinned':
        butt["inobs"] = outputdir + '/' + cfg.getValue('ctselect','output')
        butt["inmodel"] = outputdir + '/' + cfg.getValue('ctlike','output')
    elif cfg.getValue('general','anatype') == 'unbinned':
        butt["inobs"] = outputdir + '/' + cfg.getValue('ctbin','output')
        butt["inmodel"] = outputdir + '/' + cfg.getValue('ctlike','output')
        butt["expcube"]   = outputdir + '/' + cfg.getValue('ctexpcube','output')
        butt["psfcube"]   = outputdir + '/' + cfg.getValue('ctpsfcube','output')
        butt["bkgcube"]   = outputdir + '/' + cfg.getValue('ctbkgcube','output_cube')
    else:
        Utilities.warning('Unlnown type: {}'.format(cfg.getValue('general','anatype')))
        sys.exit()
        
    butt["outfile"] = outputdir + '/' + cfg.getValue('ctbutterfly','output')
    butt["emin"] = cfg.getValue('csspec','emin')
    butt["emax"] = cfg.getValue('csspec','emax')
    butt["enumbins"] = 100
    butt["srcname"] = ""
    butt["ebinalg"] = "LOG"
    if cfg.getValue('general','edisp'): 
        butt["edisp"]   = True
    else:
        butt["edisp"]   = True
    if cfg.getValue('general','debug') == True:
        butt["debug"]    = True
    
    butt.run()
    butt.save()  

