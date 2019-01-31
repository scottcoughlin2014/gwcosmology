from numpy import *
from scipy.interpolate import splev, splrep, UnivariateSpline, interp1d
from scipy.integrate import cumtrapz
from scipy.optimize import fmin

def HDI(credint, y, x):
    """Calculate the highest posterior probability interval

    Parameters:

        credint (float):
            the desired interval, must be less than 1

        y (numpy array):
            the PDF values evaluated at grid points x

        x (numpy array, same dimensions as y):
            the grid points at which the PDF values y are evaluated

    Returns:

        the two endpoints of the smallest interval which encloses credint of the posterior probability
    """
    cdfvals = cumtrapz(y,x)
    sel = cdfvals > 0.
    x = x[1:][sel]
    cdfvals = cdfvals[sel]
    cdfvals /= cdfvals[-1] #in case the posterior is not normalized
    ppf = interp1d(cdfvals,x,fill_value = 0.,bounds_error=False)
    def intervalWidth(lowTailPr):
        ret = ppf(credint + lowTailPr) - ppf(lowTailPr)
        if (ret > 0.):
            return ret
        else:
            return 1e4
    HDI_lowTailPr = fmin(intervalWidth, 1.-credint)[0]
    return ppf(HDI_lowTailPr), ppf(HDI_lowTailPr+credint)

def MAP(y, x, res = 1000):
    """Find the maximum a posteriori value

    Parameters:

        y (numpy array):
            the PDF values evaluated at grid points x

        x (numpy array, same dimensions as y):
            the grid points at which the PDF values y are evaluated

	res (int, optional)
	    the desired precision of the output in decimal places
    Returns:

        the highest-probability value
    """
    sp = UnivariateSpline(x, y, s=0.)
    x_highres = linspace(x[0], x[-1], int(around((x[-1]-x[0])*res)))
    y_highres = sp(x_highres)
    return x_highres[argmax(y_highres)]
