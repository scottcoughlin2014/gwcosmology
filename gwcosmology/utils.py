"""some basic helper functions
"""
__author__ = "smart people"

#-------------------------------------------------

def galaxy_name(graceid):
    "generate a standard filename for galaxy information"
    return "galaxy-%s.json"%graceid

def h0_name(graceid):
    "generate a standard filename for H0 posterior"
    return "H0-%s.h5"%graceid
