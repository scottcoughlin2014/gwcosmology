"""some basic helper functions
"""
__author__ = "maya.fishbach@ligo.org, reed.essick@ligo.org"

#-------------------------------------------------
distance_name = 'distance'

def galaxy_name(graceid,galaxyname):
    "generate a standard filename for galaxy information"
    return "galaxy-%s-%s.json"%(graceid,galaxyname)

def h0_name(graceid,chosen_skymap,galaxyname,PE_samples=False):
    "generate a standard filename for H0 posterior"
    skyname = chosen_skymap.split('.')[0]
    if PE_samples is False:
        return "H0-public-%s-%s-%s.json"%(graceid,skyname,galaxyname)
    if PE_samples is True:
        return "H0-proprietary-%s-%s-%s.json"%(graceid,skyname,galaxyname)

def H0_plot_name(graceid,chosen_skymap,galaxyname):
     "generate a standard filename for H0 plot"
     skyname = chosen_skymap.split('.')[0]
     return "H0-%s-%s-%s.png"%(graceid,skyname,galaxyname)
