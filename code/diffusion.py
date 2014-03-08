# Library imports
from __future__ import division
import argparse
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as la

from matplotlib import cm

# Custom libraries
import diffusion_evolve as dfe
import plotting

xnum = 52
width = 5
spacing = 0.1
alpha = 23e-6
delta_t = 10.0
h = 0.01
tolerance = 1e-20
num_env_nodes = width*2

rod = np.zeros((width, xnum))
rod.fill(293.15)

prefactor = np.zeros((xnum, xnum))
for i in range(xnum):
    for j in range(xnum):
        if i == j:
            prefactor[i,j] = 1 + 2*alpha*delta_t / h**2
        if i == j-1 or i == j+1:
            prefactor[i,j] = - alpha*delta_t / h**2
prefactor[0,0] = 1 + alpha*delta_t / h**2
prefactor[xnum-1,xnum-1] = 1 + alpha*delta_t / h**2
# The bottom and top boundary nodes only average over one neighbour at same
# point on length

pref_inv = la.inv(prefactor)

equilib_solution, num_iters = dfe.evolve_till_equilib(rod, xnum, width, pref_inv, tolerance, num_env_nodes)

plotting.plot_contour(xnum, width, spacing, equilib_solution.transpose(), filename="equilibrium.eps")
plotting.plot_surf(xnum, width, spacing, equilib_solution.transpose(), filename="equilibrium_surf.eps")

print equilib_solution