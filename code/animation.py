from __future__ import division # Division always returns float

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import types

from matplotlib import cm # matplotlib colormaps
from mpl_toolkits.mplot3d import Axes3D # 3D plotting library

# Custom libraries
import laplace_solve as lps

def laplace_anim_cont(num_x, num_y, method, ims, fig, X, Y, err_tol = 1e-2,
    max_it = 1e5, input_matrix=None, frame=None, boundary_cond=None):

    grid = np.random.rand(num_x,num_y)
    grid_new = np.zeros((num_x,num_y))
    diff = np.zeros((num_x,num_y))
    conv = np.zeros((num_x,num_y))

    plt.xlabel("$x$")
    plt.ylabel("$y$")

    num_boundary_nodes = lps.impose_boundary(grid, num_x, num_y, width=frame,
                                             conditions=boundary_cond,
                                             input_boundaries=input_matrix)

    # Iteration procedure
    num_iters = 1
    while num_iters <= max_it:

        if method == "jacobi":
            grid_new = lps.jacobi(grid, num_x, num_y)
        
        if method == "gauss-seidel":
            grid_new = lps.gauss_seidel(grid, num_x, num_y)
        
        diff = np.abs(grid_new - grid)
        
        num_iters += 1

        if lps.check_convergence(diff, err_tol, num_x, num_y, 
                             num_boundary_nodes, num_iters):

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
        lps.impose_boundary(grid, num_x, num_y, width=frame,
                            conditions=boundary_cond,
                            input_boundaries=input_matrix)

    print "Convergence condition not satisfied after {num_iters} iterations. "\
          "Try changing the number of nodes and/or grid spacing.".format(
           num_iters=num_iters)
    return False
