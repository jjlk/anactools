import sys
import os
        
import gammalib
import ctools

import anactools.Utilities as Utilities
import anactools.ConfigHandler as ConfigHandler

has_matplotlib = False

try:
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    has_matplotlib = True
except:
    has_matplotlib = False

def showSpectrum(cfg, spectrum):
    """
    Generate spectrum (points + butterfly)
    """

    outputdir = cfg.getValue('general','outputdir')
    
    if has_matplotlib == False:
        Utilities.warning('No matplotlib module ==> EXIT!!!')
        return
    
    #################################################################
    ### Taken from $CTOOLS/share/examples/python/make_spectrum.py ###
    #################################################################
    # Read spectrum file    
    table    = spectrum.table(1)
    c_energy = table["Energy"]
    c_ed     = table["ed_Energy"]
    c_eu     = table["eu_Energy"]
    c_flux   = table["Flux"]
    c_eflux  = table["e_Flux"]
    c_ts     = table["TS"]
    c_upper  = table["UpperLimit"]

    # Initialise arrays to be filled
    energies    = []
    flux        = []
    ed_engs     = []
    eu_engs     = []
    e_flux      = []
    ul_energies = []
    ul_ed_engs  = []
    ul_eu_engs  = []
    ul_flux     = []

    # Loop over rows of the file
    nrows = table.nrows()
    for row in range(nrows):

        # Get TS
        ts    = c_ts.real(row)
        flx   = c_flux.real(row)
        e_flx = c_eflux.real(row)

        # Switch
        if ts > 9.0 and e_flx < flx:

            # Add information
            energies.append(c_energy.real(row))
            flux.append(c_flux.real(row))
            ed_engs.append(c_ed.real(row))
            eu_engs.append(c_eu.real(row))
            e_flux.append(c_eflux.real(row))

        #
        else:

            # Add information
            ul_energies.append(c_energy.real(row))
            ul_flux.append(c_upper.real(row))
            ul_ed_engs.append(c_ed.real(row))
            ul_eu_engs.append(c_eu.real(row))

    # Create figure
    plt.figure()
    plt.title("Crab spectrum")

    # Plot the spectrum 
    plt.loglog()
    plt.grid()
    plt.errorbar(energies, flux, yerr=e_flux, xerr=[ed_engs, eu_engs], fmt='ro')
    if len(ul_energies) > 0:
        plt.errorbar(ul_energies, ul_flux, xerr=[ul_ed_engs, ul_eu_engs], yerr=1.0e-11, uplims=True, fmt='ro')
    plt.xlabel("Energy (TeV)")
    plt.ylabel(r"dN/dE (erg cm$^{-2}$ s$^{-1}$)")  
    
    ##################################################################
    ### Taken from $CTOOLS/share/examples/python/show_butterfly.py ###
    ##################################################################
    # Read given butterfly file    
    filename = outputdir + '/' + cfg.getValue('ctbutterfly','output')
    csv      = gammalib.GCsv(filename)

    # Initialise arrays to be filled
    butterfly_x = []
    butterfly_y = []
    line_x      = []
    line_y      = []

    # Loop over rows of the file
    nrows = csv.nrows()
    for row in range(nrows):

        # Compute upper edge of confidence band
        butterfly_x.append(csv.real(row,0)*1.e-6) ## JLK MeV -> TeV
        #butterfly_y.append(csv.real(row,2)*1.e6) ## JLK MeV -> TeV
        scale = csv.real(row,0)*csv.real(row,0)*1.e-6*1.6
        butterfly_y.append(csv.real(row,2)*scale) ## JLK MeV -> TeV -> erg

        # Set line values
        line_x.append(csv.real(row,0)*1.e-6) ## JLK MeV -> TeV
        line_y.append(csv.real(row,1)*scale) ## JLK MeV -> TeV -> erg

    # Loop over the rows backwards to compute the lower edge
    # of the confidence band    
    for row in range(nrows):
        
        index = nrows - 1 - row
        butterfly_x.append(csv.real(index,0)*1.e-6) ## JLK MeV -> TeV
        scale = csv.real(index,0)*csv.real(index,0)*1.e-6*1.6
        low_error = csv.real(index,3)*scale ## JLK MeV -> TeV -> erg

        if low_error < 1e-26:
            low_error = 1e-26
        butterfly_y.append(low_error)   

    plt.fill(butterfly_x,butterfly_y,color='green',alpha=0.5)
    plt.plot(line_x,line_y,color='black',ls='-')

    outputdir = cfg.getValue('general','outputdir')
    plt.savefig(outputdir + '/' + cfg.getValue('plots','spec_outfile'))
    #plt.show()

