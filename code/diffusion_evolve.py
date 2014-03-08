# Library imports
from __future__ import division

import numpy as np
from numpy import linalg as la
import sys

def check_equilib(rod, evolved_rod, xnum, width, tolerance, num_env_nodes, iter_num):

    equilib_check = np.abs(evolved_rod - rod) < tolerance

    num_nodes = xnum*width
    num_equilib = np.sum(equilib_check)

    sys.stdout.flush()
    sys.stdout.write("\rNumber of nodes converged: %5d / %5d;"\
                     "\tNumber of iterations: %6d" % 
                     (num_equilib, num_nodes - num_env_nodes, iter_num))

    if num_equilib >= num_nodes - num_env_nodes:
        print
        return True

    return False

def iterate(rod, xnum, pref_inv):
    
    rod_new = rod.dot(pref_inv)
    # Faster than using np.solve(a,b), because inverse already calculated
    
    return rod_new

def evolve(rod, xnum, pref_inv):
    
    rod[:,0] = 1273.15
    rod[:,xnum-1] = 273.15

    evolved_rod = iterate(rod, xnum, pref_inv)
    
    return evolved_rod 

def evolve_till_equilib(rod, xnum, width, pref_inv, tolerance, num_env_nodes):

    k = 0
    while k <= 1e6:
        evolved_rod = evolve(rod, xnum, pref_inv)

        if check_equilib(rod, evolved_rod, xnum, width, tolerance, num_env_nodes, k):
            print "Successfully found equilibrium after {} iterations.".format(k+1)
            return evolved_rod, k

        rod = np.copy(evolved_rod)

        sys.stdout.flush()
        sys.stdout.write("\rNumber of iterations completed: %5d" % (k+1))

        k += 1

    return False, False