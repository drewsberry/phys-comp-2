# Library imports
from __future__ import division

import argparse
import math
import numpy as np
from numpy import linalg as la

# Custom libraries
import diffusion_evolve as dfe
import plotting
import matrix_io as mio

parser = argparse.ArgumentParser(description="Solving heat diffusion equation for iron rod.")

parser.add_argument("-w", "--width", type=int, default=25,
                    help="specify width of iron rod. Default is 5 cm.")
# Adding two-dimensionality with width does not affect heat diffusion but makes it more
# representative of a physical situation.

parser.add_argument("-s", "--timestep", type=float, default=0.1,
                    help="specify time step for each iteration.")

parser.add_argument("-t", "--time", type=float, default=100,
                    help="specify length of time in seconds to simulate.")

parser.add_argument("-e", "--error", type=float, default=1e-5,
                    help="specify absolute error tolerance in kelvin for equilibrium check.")

parser.add_argument("-c", "--cold", action="store_true",
                    help="dip other end of rod in ice at 0 degrees celsius.")

parser.add_argument("-q", "--equilibrium", action="store_true",
                    help="keep on iterating until equilibrium state is found. "\
                         "If chosen, results in '--time' option being ignored.")

parser.add_argument("-p", "--plot", choices=["normal", "contour", "surface"], nargs="*",
                    help="plot resulting temperature solutions to eps file.")

parser.add_argument("-o", "--output",
                    help="write output temperature solution to file.")

parser.add_argument("-r", "--printout", action="store_true",
                    help="print resulting grid of temperatures to stdout.")

args = parser.parse_args()

# Constants
room_temp = 293.15
furnace_temp = 1273.15
ice_temp = 273.15
diffusivity = 23e-6

# Chosen grid variables
xnum = 52 # Grid is 50cm long with 2 extra nodes for the environment
spacing = 0.01 # Nodes are 1cm apart
num_env_nodes = args.width # Hot end only

num_iters = int(math.ceil(args.time / args.timestep))
# Number iterations to simulate correct time; needs be integer

if args.cold == True:
    num_env_nodes = args.width*2 # Cold end also

rod = np.zeros((args.width, xnum))
rod.fill(room_temp)
# Rod starts off at room temperature

prefactor = np.zeros((xnum, xnum))
for i in range(xnum):
    for j in range(xnum):
        if i == j:
            prefactor[i,j] = 1 + 2*diffusivity*args.timestep / spacing**2
        if i == j-1 or i == j+1:
            prefactor[i,j] = - diffusivity*args.timestep / spacing**2

prefactor[0,0] = 1 + diffusivity*args.timestep / spacing**2
prefactor[xnum-1,xnum-1] = 1 + diffusivity*args.timestep / spacing**2
# The bottom and top boundary nodes only average over one neighbour at same
# point on length

pref_inv = la.inv(prefactor)
# Inverting once at beginning and passing as argument is hugely more efficient

if args.equilibrium:
    solution, iters_needed = dfe.evolve_till_equilib(rod, xnum, args.width,
                                                     pref_inv, args.error, 
                                                     num_env_nodes, cold=args.cold)
    if iters_needed:
        time_needed = iters_needed*args.timestep

        print "\nTime needed to reach equilibrium: {} seconds.".format(time_needed)

if not args.equilibrium:
    solution = dfe.evolve(rod, xnum, pref_inv, num_iters, cold=args.cold)

if args.output:
    print "Printing temperature solution to file "\
          "{}.dat".format(args.output),
    mio.print_matrix_to_file(solution, args.output+".dat")
    print "...done"

if args.printout:
    print "\nPrinting temperature solution to stdout..."
    mio.print_matrix(solution)
    print "...done"

if args.plot:
    for i in range(len(args.plot)):
        if args.plot[i] == "normal":
            plotting.plot_normal(xnum, solution, filename="rod_normal")
        if args.plot[i] == "contour":
            plotting.plot_contour(xnum, args.width, spacing, solution.transpose(), 
                                  title="phi", filename="rod_contour")
        if args.plot[i] == "surface":
            plotting.plot_surface(xnum, args.width, spacing, solution.transpose(), 
                                  title="phi", filename="rod_surface")
        # The title is just a way of making subtly different plots for the Laplace 
        # and heat diffusion sections with the same reusable plotting code.
