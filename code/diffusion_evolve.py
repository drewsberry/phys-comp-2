# Library imports
from __future__ import division

import numpy as np
import sys

def impose_hot_end(rod, xnum):
    # Impose the boundary condition that end in furnace is 1000 degrees Celsius.

    rod[:,0] = 1273.15

    return rod

def impose_cold_end(rod, xnum):
    # Impose boundary condition that end in ice is 0 degrees Celsius.

    rod[:,xnum-1] = 273.15

    return rod

def check_equilib(rod, evolved_rod, xnum, width, tolerance, num_env_nodes, iter_num):
    # Check to see whether all nodes of rod have reached equilibrium.

    equilib_check = np.abs(evolved_rod - rod) < tolerance

    num_nodes = xnum*width
    num_equilib = np.sum(equilib_check)

    sys.stdout.flush()
    sys.stdout.write("\rNumber of nodes in equilibrium: %5d / %5d;"\
                     "\tNumber of iterations completed: %6d" % 
                     (num_equilib, num_nodes - num_env_nodes, 
                      iter_num+1))

    if num_equilib >= num_nodes - num_env_nodes:
        print
        return True

    return False

def iterate(rod, xnum, pref_inv):
    # Solve the linear system of equations derived from the implicit finite
    # difference equation to advance time by the time step.
    
    rod_new = rod.dot(pref_inv)
    # Faster than using np.solve(a,b), because inverse already calculated
    
    return rod_new

def evolve(rod, xnum, pref_inv, num_iters, cold=False):
    # Evolve the system a specified number of times 'num_iters'.

    impose_hot_end(rod, xnum)

    if cold:
        impose_cold_end(rod, xnum)
    
    for counter in range(num_iters):

        evolved_rod = iterate(rod, xnum, pref_inv)

        rod = np.copy(evolved_rod)

        impose_hot_end(rod, xnum)

        if cold:
            impose_cold_end(rod, xnum)

        sys.stdout.flush()
        sys.stdout.write("\rNumber of iterations completed: %5d / %5d" % 
                         (counter+1, num_iters))
    
    print
    return rod 

def evolve_till_equilib(rod, xnum, width, pref_inv, tolerance, num_env_nodes, cold=False, max_iters=1e6):
    # Evolve the system until equilibrium is reached to a certain tolerance, as per check_equilib().

    max_iters = int(max_iters)

    impose_hot_end(rod, xnum)

    if cold:
        impose_cold_end(rod, xnum)

    for counter in range(max_iters):

        evolved_rod = iterate(rod, xnum, pref_inv)

        if check_equilib(rod, evolved_rod, xnum, width, tolerance, num_env_nodes, counter):
            print "Successfully found equilibrium after {} iterations.".format(counter+1)
            return evolved_rod, counter

        rod = np.copy(evolved_rod)

        impose_hot_end(rod, xnum)

        if cold:
            impose_cold_end(rod, xnum)
        # Boundary conditions need to be reimposed after each iteration.

    print "Equilibrium not found after {} iterations.".format(counter)
    return False, False
