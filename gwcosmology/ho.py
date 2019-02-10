import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import norm
from astropy.cosmology import FlatLambdaCDM 
import astropy.units as u
import healpy as hp

def dist_from_skymap(fname,ra, dec, num_samples = 128):
     """
     Parameters:
         fname (string):
             name of the skymap file
         ra (float):
             RA of the counterpart (in degrees)
         dec (float):
             DEC of the counterpart (in degrees)
         num_samples (int, optional):
             number of distance samples to return
     """
     fname = str(fname)
     skymap, distmu, distsigma, distnorm = hp.read_map(fname,field=[0,1,2,3])
     npix = len(distmu)
     nside = hp.npix2nside(npix)
     pixel = hp.ang2pix(nside, np.pi/2.0-dec*np.pi/180.0,ra*np.pi/180.0)
     mu = distmu[pixel]
     sigma = distsigma[pixel]
     num = 0
     post_samps = np.array([])
     while num < num_samples:
     	lkhd_samps =  sigma*np.random.randn(num_samples*2)+mu
     	prior_wts = lkhd_samps**2
     	rs = np.random.uniform(low=0.0, high = max(prior_wts),size = prior_wts.size)
     	sel = rs < prior_wts
        post_samps = np.append(post_samps,lkhd_samps[sel])
        post_samps[post_samps<0] = 0.0
        num = len(post_samps)
     return post_samps[0:num_samples]


def setup_cosmo(Om0 = 0.3, H0_default = 70.0, z_min = 0.0, z_max = 0.1, z_res = 0.0005):
    """
    Parameters:

        Om0 (float, optional): 
            the value of Omega_matter today for the input flat cosmology, default is 0.3 
    """
    cosmo = FlatLambdaCDM(H0 = H0_default, Om0 = Om0)
    z_interp = np.linspace(z_min,z_max,np.round((z_max-z_min)/z_res))
    z_at_dL = interp1d(cosmo.luminosity_distance(z_interp).to('Mpc').value, z_interp)
    return z_at_dL

def measure_H0(distance_posterior, z_mean, z_std,z_at_dL, H0_default,
               hmin=10.0, hmax=250.0, h0_res = 1.0):
    """Calculate H0 posterior

    Parameters:

        distance_posterior (array):
            distance posterior samples

        z_mean (float):
            observed redshift of (the host galaxy to) the counterpart, corrected by peculiar velocities

        z_std (float):
            standard deviation of the redshift measurement
        
        z_at_dL (function):
            function that returns redshift value for a given luminosity distance in Mpc

        H0_default (float):
            default H0 value in km/s/Mpc used for z_at_dL function

        hmin (float, optional):
            minimum of H0 prior (km/s/Mpc); default 10

        hmax (float, optional):
            maximum of H0 prior (km/s/Mpc); default 250

	h0_res (float, optional):
	    resolution of the H0 grid on which to evaluate the posterior; default is 1 km/s/Mpc precision


    Returns:
        the posterior PDF of H0, using a flat prior between hmin and hmax
    """
    hs = np.linspace(hmin,hmax,np.round((hmax-hmin)/h0_res))
    lh = np.zeros_like(hs)
    for i, h in enumerate(hs):
        lh[i] = np.mean(norm.pdf(z_at_dL(distance_posterior*h/H0_default),loc=z_mean, scale=z_std))
    lh = lh/np.trapz(lh,hs)
    return hs, lh

def measure_H0_from_skymap(fname, z_mean, z_std,ra, dec, Om0, H0_default, z_res, hmin, hmax, h0_res):
     #z_min = np.maximum((z_mean - 5.0*z_std)*hmin/H0_default,0.0)
     z_min = 0.0
     z_max = (z_mean+5.0*z_std)*hmax/H0_default
     z_at_dL = setup_cosmo(Om0, H0_default, z_min, z_max, z_res)
     distance_posterior = dist_from_skymap(fname,ra, dec, num_samples = 128)
     hs, lh = measure_H0(distance_posterior, z_mean, z_std, z_at_dL, H0_default, hmin, hmax, h0_res)
     return hs, lh
