import numpy as np
import matplotlib.pyplot as plt
import h5py
from gwcosmology.utils import H0_plot_name

def read_ho_likelihood(fname):
     "takes the hdf5 file containing the H0 likelihood for a single event and plots it"
     with h5py.File(str(fname),'r') as inp:
          lh = np.array(inp['H0'])
          hs = float(inp['H0'].attrs['H0_start'])+float(inp['H0'].attrs['dH0'])*np.arange(inp['H0'].attrs['num_H0'])
          skymap_file = str(inp['H0'].attrs['skymap_file'])
          gid = str(inp['H0'].attrs['graceid'])
     return hs, lh
     #plt.plot(hs,lh)
     #plt.xlabel('H0')
     #plt.ylabel('p(H0)')
     #change this to return figure object
     #plt.savefig(H0_plot_name(gid,skymap_file)) 
