# Library imports
from __future__ import division

import numpy as np
from numpy import linalg

def iterate(rod, xnum, prefactor):
    
    # print "rod shape: ", rod.shape
    # print "prefactor shape: ", prefactor.shape

    rod_new = linalg.solve(prefactor, rod)
    
    return rod_new

def evolve(rod, xnum, prefactor):
    
    rod[0,:] = 1273.15

    evolved_rod = iterate(rod, xnum, prefactor)
    
    # print "Evolved rod:"
    # print evolved_rod 

    return evolved_rod 
