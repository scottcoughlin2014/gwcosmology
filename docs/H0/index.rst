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

    In [1]: from gwcosmology.ho import ho

    In [2]: from gwcosmology.stats import stats

    In [3]: import numpy

    In [3]: import seaborn as sns

    In [3]: import matplotlib.pyplot as plt

    In [2]: post_lows = numpy.genfromtxt('../data/posterior_samples_RR30.dat', names=True)

    In [3]: post_highs = numpy.genfromtxt('../data/posterior_samples_RR31.dat', names=True)

    In [4]: from scipy.stats import gaussian_kde

    In [5]: ppdL_highs = gaussian_kde(post_highs['distance'])

    In [6]: ppdL_lows = gaussian_kde(post_lows['distance'])

    In [5]: hs,lh_highs = ho.measure_H0(ppdL_highs) 

    In [6]: hs,lh_lows = ho.measure_H0(ppdL_lows) 

    In [3]: posth_highs = lh_highs / hs / numpy.trapz(lh_highs/hs, hs)

    In [3]: posth_lows = lh_lows / hs /numpy.trapz(lh_lows/hs, hs)

    In [3]: plt.plot(hs, posth_highs, label='high-spin run')

    In [3]: plt.plot(hs, posth_lows, label='low-spin run')

    In [3]: ymin, ymax = plt.gca().get_ylim()

    In [3]: plt.axvline(ho.planck_h, label='Planck', color=sns.color_palette()[2])

    In [3]: plt.fill_betweenx([ymin,ymax], ho.planck_h - 2*ho.sigma_planck_h, ho.planck_h + 2*ho.sigma_planck_h, color=sns.color_palette()[2], alpha=0.2)

    In [3]: plt.axvline(ho.riess_h, label='SHoES', color=sns.color_palette()[3])

    In [3]: plt.fill_betweenx([ymin,ymax], ho.riess_h - 2*ho.sigma_riess_h, ho.riess_h + 2*ho.sigma_riess_h, color=sns.color_palette()[3], alpha=0.2)

    In [3]: plt.legend(loc='best')

    In [3]: plt.xlim(40,180)

    In [3]: plt.ylim(ymin,ymax)

    In [3]: plt.xlabel(r'$H_0$ (km/s/Mpc)')

    In [3]: plt.ylabel(r'$p(H_0)$ (km$^{-1}$ s Mpc)')

    @savefig plot-h0.png
    In [22]: plt


=====
Stats
=====

.. ipython::

    In [3]: MAP_highs = stats.MAP(posth_highs,hs)

    In [3]: a_highs, b_highs = stats.HDI(0.683,posth_highs,hs)

    In [3]: MAP_lows = stats.MAP(posth_lows,hs)

    In [3]: a_lows, b_lows = stats.HDI(0.683,posth_lows,hs)

    In [3]: print('high spin prior: H0 = {0} + {1} - {2} (MAP and 68.3 percent HDI)'.format(MAP_highs,b_highs-MAP_highs,MAP_highs-a_highs))

    In [3]: print('low spin prior: H0 = {0} + {1} - {2} (MAP and 68.3 percent HDI)'.format(MAP_lows,b_lows-MAP_lows,MAP_lows-a_lows))
