from astropy import constants as const
from numpy import *
import cosmolopy.distance as cd
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

def HDI(credint, y, x):
    """Measure H0

    Parameters:

        credint (float):
            trigger time of event to be processing

        y (float):
            length of data to be processed

        x (float):
            required data channels.

    Returns:

        H0
    """
    cdfvals = cumtrapz(y,x)
    sel = cdfvals > 0.
    x = x[1:][sel]
    cdfvals = cdfvals[sel]
    ppf = interp1d(cdfvals,x,fill_value = 0.,bounds_error=False)
    def intervalWidth(lowTailPr):
        ret = ppf(credint + lowTailPr) - ppf(lowTailPr)
        if (ret > 0.):
            return ret
        else:
            return 1e4
    HDI_lowTailPr = fmin(intervalWidth, 1.-credint)[0]
    return ppf(HDI_lowTailPr), ppf(HDI_lowTailPr+credint)

def MAP(y, x):
    """Measure H0

    Parameters:

        y (float):
            trigger time of event to be processing

        x (float):
            length of data to be processed

    Returns:

        H0
    """
    sp = UnivariateSpline(x,y,s=0.)
    x_highres = linspace(hmin,hmax,100000)
    y_highres = sp(x_highres)
    return x_highres[argmax(y_highres)]
