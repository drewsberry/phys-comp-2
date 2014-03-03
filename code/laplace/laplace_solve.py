# Library imports
from __future__ import division # Division always returns float

import numpy as np
import sys

def impose_boundary(grid, num_x, num_y, input_boundaries=None, conditions=None):
    # Set the specified boundary conditions, with known in-built conditions and
    # return number of boundary nodes.

    if conditions == "capacitor":
        grid[num_x/4,:] = 1
        grid[3*num_x/4,:] = -1

        return 2*num_y

    if conditions == "point_charge":
        grid[num_x/2,num_y/2] = 1

        return 1

    if conditions == "plane":
        grid[num_x/2,:] = 1

        return num_y

    if conditions == "net":
        grid[0,:] = 1
        grid[num_x-1,:]  =1
        grid[:,0] = 1
        grid[:,num_y-1] = 1

        return 2*num_x + 2*num_y

    if conditions == "cross":
        grid[num_x/2,:] = 1
        grid[:,num_y/2] = 1
        # print_matrix(grid)

        return num_x + num_y - 1

    if input_boundaries is not None:
        num_boundary_nodes = 0

        num_cols = input_boundaries.shape[0]
        num_rows = input_boundaries.shape[1]

        for i in range(num_rows):
            for j in range(num_cols):
                if input_boundaries[j,i] != "None":
                    grid[i,j] = input_boundaries[j,i]
                    num_boundary_nodes += 1

        return num_boundary_nodes

    return 0

def check_convergence(diff, epsilon, num_x, num_y, num_boundary_nodes, iter_num):
    # Check for convergence at absolute error epsilon

    num_nodes = num_x*num_y

    conv = diff < epsilon

    # Num converged entries is sum of all true values of convergence matrix
    num_converged = np.sum(conv)

    # Write node convergence progress to stdout
    sys.stdout.flush()
    sys.stdout.write("\rNumber of nodes converged: %5d / %5d;"\
                     "\tNumber of iterations: %6d" % 
                     (num_converged, num_nodes - num_boundary_nodes, iter_num))
    
    # Set boundary nodes are reset so won't converge, but all others must
    if num_converged >= num_nodes - num_boundary_nodes:
        print
        return True

    return False

def iterate_node(grid, i, j, num_x, num_y):
    # Apply iteration technique for i,j element of matrix grid and save value
    # into grid_new

    above = grid[i,j+1] if j < num_y-1 else 0
    below = grid[i,j-1] if j > 0 else 0
    right = grid[i+1,j] if i < num_x-1 else 0
    left  = grid[i-1,j] if i > 0 else 0

    return (above + below + left + right) / 4
    
def jacobi(grid, num_x, num_y):
    # Apply iterate_node() to grid, using the Jacobi iteration method, requiring two grids. Return the new grid obtained by iterating over each node.
    
    grid_new = np.zeros((num_x, num_y))
    
    for i in range(0,num_x):
        for j in range(0,num_y):
            
            grid_new[i,j] = iterate_node(grid, i, j, num_x, num_y)
            
    return grid_new
    
def gauss_seidel(grid, num_x, num_y):
    # Apply iterate_node() to grid, using the Gauss-Seidel iteration method, requiring only one grid. Return the grid obtained by iterating over the whole matrix.
    
    for i in range(0,num_x):
        for j in range(0,num_y):
            
            grid[i,j] = iterate_node(grid, i, j, num_x, num_y)
            
    return grid
    # CHECK TO MAKE SURE THIS IS THE CORRECT WAY TO DO THE GAUSS-SEIDEL METHOD, IT PROBABLY ISN'T

def solve(num_x, method, num_y, err_tol = 1e-2, max_it = 1e5, input_matrix=None, boundary_cond=None):

    grid = np.random.rand(num_x,num_y)
    grid_new = np.zeros((num_x,num_y))
    diff = np.zeros((num_x,num_y))
    conv = np.zeros((num_x,num_y))

    num_boundary_nodes = impose_boundary(grid, num_x, num_y, 
                                         conditions=boundary_cond,
                                         input_boundaries=input_matrix)

    # Iteration procedure
    num_iters = 1
    while num_iters <= max_it:
        #for i in range(0,num_x):
        #    for j in range(0,num_y):

        #        grid_new[i,j] = iterate_node(grid, i, j, num_x, num_y)
        #        diff[i,j] = np.abs(grid_new[i,j] - grid[i,j])

        if method == "jacobi":
            grid_new = jacobi(grid, num_x, num_y)
        
        if method == "gauss":
            grid_new = gauss_seidel(grid, num_x, num_y) # I don't think this is how Gauss-Seidel methods works
        
        diff = np.abs(grid_new - grid)
        
        num_iters += 1

        if check_convergence(diff, err_tol, num_x, num_y, 
                             num_boundary_nodes, num_iters):
            print "Convergence condition of all changes less than absolute "\
                  "error {tolerance} satisfied after {iters} iterations".format(
                    tolerance=err_tol,iters=num_iters)
            return grid

        grid = np.copy(grid_new)

        # Boundary conditions must remain set for all iterations
        impose_boundary(grid, num_x, num_y, conditions=boundary_cond,
                        input_boundaries=input_matrix)

    print "Convergence condition not satisfied after {num_iters} iterations. "\
          "Try changing the number of nodes and/or grid spacing.".format(
           num_iters=num_iters)
    return False
