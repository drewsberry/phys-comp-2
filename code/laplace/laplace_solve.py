# Library imports
from __future__ import division # Division always returns float

import numpy as np
import sys
import os.path

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

        for i in range(num_cols):
            for j in range(num_rows):
                if input_boundaries[i,j] != "None":
                    grid[i,j] = input_boundaries[i,j]
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

def print_matrix(matrix):
    # Print matrix neatly to stdout

    num_cols = matrix.shape[0]
    num_rows = matrix.shape[1]

    for i in range(num_cols):
        for j in range(num_rows):
            sys.stdout.write("%6f" % matrix[i,j])
            if j != num_rows:
                sys.stdout.write(", ")
        print

def print_matrix_to_file(matrix, filename):
    # Take NumPy 2D array and print it to file for external verification/plotting

    if os.path.isfile(filename):
        response = str(raw_input("Warning, chosen output file already exists. Overwrite? "))
        if response.lower() == "yes":
            print "Continuing..."
        elif response.lower() == "no":
            print "Aborting... "
            exit(2)
        else:
            print "Unrecognised response. Aborting..."
            exit(3)

    output_file = open(filename, 'w')

    num_cols = matrix.shape[0]
    num_rows = matrix.shape[1]

    try:
        for i in range(num_cols):
            for j in range(num_rows):
                output_file.write("%6f\t" % matrix[i,j])
            output_file.write("\n")

    finally:
        output_file.close()
    # Ensure file is properly closed, even if writing to file fails

def input_matrix(filename):
    # Return array contained in filename

    input_file = open(filename,"r")

    num_cols = len(input_file.readline().split())
    input_file.seek(0)

    num_rows = sum(1 for line in input_file)
    input_file.seek(0)

    matrix = np.array([[None for i in range(num_cols)] 
                             for i in range(num_rows)])
    line_num = 0

    while True:
        line = input_file.readline()
        if not line: break
        matrix[line_num,:] = line.split()
        line_num += 1

    input_file.close()

    return matrix, num_cols, num_rows

def solve(num_x, num_y, err_tol = 1e-2, max_it = 1e5, input_matrix=None, boundary_cond=None):

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
        for i in range(0,num_x):
            for j in range(0,num_y):

                grid_new[i,j] = iterate_node(grid, i, j, num_x, num_y)
                diff[i,j] = np.abs(grid_new[i,j] - grid[i,j])

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
