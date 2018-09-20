from astropy import constants as const
from numpy import *
from scipy.interpolate import splev, splrep, UnivariateSpline, interp1d
from scipy.integrate import cumtrapz
from scipy.stats import gaussian_kde, norm
from astropy.cosmology import Planck15 as cosmo 
from astropy.cosmology import z_at_value
import astropy.units as u
import seaborn as sns
from scipy.optimize import fmin

c = const.c.to('km/s').value
v_hubble = 3017.
v_hubble_std = (72.**2 + 150.**2)**0.5
planck_h = 67.74
sigma_planck_h = 0.46
riess_h = 73.24
sigma_riess_h = 1.74


def measure_H0(distance_posterior, z_mean=v_hubble/c, z_std=v_hubble_std/c,
               hmin=10, hmax=250):
    """Measure H0

    Parameters:

        distance_posterior (array):
            required data channels.

        z_mean (float):
            trigger time of event to be processing

        z_std (float):
            length of data to be processed

        hmin (int, optional):
            sample rate of the data desired

        hmax (int, optional):
            name of frametype in which this channel is stored, by default
            will search for all required frame types

    Returns:

        H0
    """
    hs = linspace(hmin,hmax,600)
    lh = zeros(size(hs))
    ds = linspace(5,60,150)
    zs = zeros((size(hs),size(ds)))
    for i, h in enumerate(hs):
        for j, d in enumerate(ds):
            #zs[i,j] = z_at_value(cosmo.luminosity_distance,d*u.Mpc*cosmo.H(0).value/(100*h))
            zs[i,j] = d*h/c
        lh[i] = trapz(norm.pdf(zs[i],
                               loc=z_mean,scale=z_std) * 
                      distance_posterior.evaluate(ds), ds)
    lh = lh/trapz(lh,hs)
    return hs, lh
