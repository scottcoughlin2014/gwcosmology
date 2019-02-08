from numpy import *

def HDI(credint, pdfs, xs):
    """Calculate the highest posterior probability interval by a waterfilling algorithm

    Parameters:

        credint (float):
            the desired interval, must be less than 1

        pdfs (numpy array):
            the PDF values evaluated at grid points x

        xs (numpy array, same dimensions as y):
            the grid points at which the PDF values y are evaluated

    Returns:

        the two endpoints of the smallest interval which encloses credint of the posterior probability
    """
    order = argsort(pdfs)[::-1] #largest to smallest
    last_index = len(pdfs)-1
    mass = 0.0
    for n in order:
        if n==0:
            mass+=0.5*pdfs[0]*(xs[1]-xs[0])
        if n==last_index:
            mass+=0.5*pdfs[-1]*(xs[-2]-xs[-1])
        else:
            mass+=0.5*pdfs[n]*(xs[n+1]-xs[n-1])
        if mass >= credint:
            print mass
            pdf_thresh = pdfs[n]
            print pdf_thresh
            break
    idx1 = argmax(pdfs>=pdf_thresh)
    idx2 = argmax(pdfs[::-1]>=pdf_thresh)
    return xs[idx1], xs[::-1][idx2]

def MAP(y, x, res = 100):
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

def credible_levels(ps, fs):
    """Find the probability levels that correspond to a given array of credible levels, e.g. to then pass into the levels argument of a contour plot
    Parameters:
       ps (1-d numpy array):
          the PDF values, a flattened array
       fs (1-d numpy array):
          the desired credibile levels in ascending order, e.g. array([0.5,0.9]) for 50% and 90% credible levels
    """
    sorter = argsort(ps)
    ps_sorted = ps[sorter]
    ps_sorted = ps_sorted[::-1] #largest to smallest
    csum = cumsum(ps_sorted)
    idxs = searchsorted(csum,fs*csum[-1])
    levels = ps_sorted[idxs]
    levels = levels[::-1]
    return levels
