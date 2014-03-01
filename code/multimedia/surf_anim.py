from __future__ import division # Division always returns float

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys

from matplotlib import cm # matplotlib colormaps
from mpl_toolkits.mplot3d import Axes3D # 3D plotting library

def impose_boundary(grid, width):
    # Set the specified boundary conditions, with known in-built conditions

    global num_boundary_nodes

    grid[num_x/4, num_y/2 - width:num_y/2 + width] = 1
    grid[3*num_x/4, num_y/2 - width:num_y/2 + width] = -1

    num_boundary_nodes = 1 + 4*width

    return grid

def check_convergence(diff, epsilon):
    # Check for convergence at absolute error epsilon

    # Boolean convergence matrix
    conv = diff < epsilon

    # Num converged entries is sum of all true values of convergence matrix
    num_converged = np.sum(conv)

    # Write node convergence progress to stdout
    sys.stdout.flush()
    sys.stdout.write("\rNumber of nodes converged: %5d / %5d;\tFrame number: "\
        "%2d / %2d" % (num_converged, num_nodes - num_boundary_nodes,
            len(ims), num_frames))
    
    # Set boundary nodes are reset so won't converge, but all others must
    if num_converged >= num_nodes - num_boundary_nodes:
        return True

    return False

def iterate_node(grid, i, j):
    # Apply iteration technique for i,j element of matrix grid and save value
    # into grid_new

    above = grid[i,j+1] if j < num_y-1 else 0
    below = grid[i,j-1] if j > 0 else 0
    right = grid[i+1,j] if i < num_x-1 else 0
    left  = grid[i-1,j] if i > 0 else 0

    return (above + below + left + right) / 4

def solve(num_x, num_y, width, epsilon = 1e-2, max_it = 1e5):

    # Fill with zeros important matrices used later
    grid_new = np.zeros((num_x,num_y))
    diff = np.zeros((num_x,num_y))

    surf_axes = fig.gca(projection='3d')
    surf_axes.set_xlabel("$x$")
    surf_axes.set_ylabel("$y$")

    # Fill grid with random guesses between 0 and 1
    grid = np.random.rand(num_x,num_y)

    impose_boundary(grid, width)

    # Iteration procedure
    k = 1
    while k <= max_it:
        for i in range(0,num_x):
            for j in range(0,num_y):

                grid_new[i,j] = iterate_node(grid, i, j)
                diff[i,j] = np.abs(grid_new[i,j] - grid[i,j])

        k += 1

        if check_convergence(diff, epsilon) == True:

            surf_plot = surf_axes.plot_surface(X, Y, grid_new.transpose(), 
                rstride=1, cstride=1, cmap=cm.hot, linewidth=0)

            ims.append([surf_plot])

            return grid

        grid = np.copy(grid_new)

        # Boundary conditions must remain set for all iterations
        impose_boundary(grid, width)

    print "Convergence condition not satisfied after {k} iterations. "\
        "Try changing the number of nodes and/or grid spacing.".format(k=k)
    return False

num_x = 100
num_y = 100
h = 1/16

num_nodes = num_x*num_y

ims = []

x = np.linspace(0, num_x*h, num_x)
y = np.linspace(0, num_y*h, num_y)  
X, Y = np.meshgrid(x,y)

fig = plt.figure()
fig.suptitle("$\\varphi(x,y)$")

num_frames = 50
for width in range(1,num_frames):
    solution = solve(num_x, num_y, width)

print "Iterations finished. Creating animation."
capacitor_anim = anim.ArtistAnimation(fig, ims, interval=100, blit=False)
print "Animation made. Saving to file."

capacitor_anim.save("surf_anim.mp4")
print "Animation saved to file as {filename}.".format(filename="surf_anim.mp4")
