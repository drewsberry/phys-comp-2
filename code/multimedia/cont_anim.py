from __future__ import division # Division always returns float

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import types
import sys

from matplotlib import cm # matplotlib colormaps
from mpl_toolkits.mplot3d import Axes3D # 3D plotting library

# Custom libraries
import laplace_solve as lps
import plotting

def solve(num_x, num_y, width, epsilon = 1e-2, max_it = 1e5):

    # Fill with zeros important matrices used later
    grid_new = np.zeros((num_x,num_y))
    diff = np.zeros((num_x,num_y))

    plt.xlabel("$x$")
    plt.ylabel("$y$")

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

            cont_plot = plt.contourf(X, Y, grid.transpose(), 100, rstride=1, cstride=1,
                cmap=cm.hot)

            # Duck punch from matplotlib mailing list
            def setvisible(self,vis):
                for c in self.collections: c.set_visible(vis) 
            cont_plot.set_visible = types.MethodType(setvisible,cont_plot,None) 
            cont_plot.axes = plt.gca() 
            cont_plot.figure = fig

            ims.append([cont_plot])

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
plt.colorbar()
print "Animation made. Saving to file."

capacitor_anim.save("cont_anim.mp4")
print "Animation saved to file as {filename}.".format(filename="cont_anim.mp4")
