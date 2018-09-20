.. _H0:

############
Calculate H0
############

============
Introduction
============

==
H0
==


.. ipython::

    In [1]: from gwcosmology.ho.ho import measure_H0

    In [2]: from gwcosmology.stats.stats import HDI

    In [3]: import numpy

    In [2]: post_lows = numpy.genfromtxt('../data/posterior_samples_RR30.dat',names=True)

    In [3]: post_highs = numpy.genfromtxt('../data/posterior_samples_RR31.dat',names=True)

    In [4]: from scipy.stats import gaussian_kde

    In [5]: ppdL_highs = gaussian_kde(post_highs['distance'])

    In [6]: ppdL_lows = gaussian_kde(post_lows['distance'])

    In [5]: hs,lh_highs = measure_H0(ppdL_highs) 

    In [5]: print(hs, lh_highs) 

    In [6]: hs,lh_lows = measure_H0(ppdL_lows) 

    In [5]: print(hs, lh_highs, lh_lows) 
